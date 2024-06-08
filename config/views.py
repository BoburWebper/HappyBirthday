from datetime import datetime

from aiogram.types import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserBirthdays, UserBirthdayImages, TelegramUsers, StaffUser


@login_required
def home(request):
    today = datetime.now().date()
    birthdays = UserBirthdays.objects.all()
    staffs = StaffUser.objects.all()
    birthdays_with_users = []

    for birthday in birthdays:
        user = TelegramUsers.objects.get(telegram_id=birthday.telegram_id)
        user_images = UserBirthdayImages.objects.filter(user_birthday_id=birthday.birthday_id)
        birthdays_with_users.append({'birthday': birthday, 'user': user, 'images': user_images})
        birthdays_with_users.reverse()

    return render(request, 'index.html', {'birthdays_with_users': birthdays_with_users, 'staffs': staffs})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home')
        else:
            # Check if username and password match any staff user
            try:
                staff_user = StaffUser.objects.get(username=username, password=password)
                request.session['staff_user_id'] = staff_user.id
                return redirect('profile')
            except StaffUser.DoesNotExist:
                return HttpResponse("Invalid username or password")
    else:
        return render(request, 'login.html')


def profile_view(request):
    # Retrieve staff user ID from session
    staff_user_id = request.session.get('staff_user_id')
    all_birthday_data = []
    # Check if staff user ID is stored in session
    if staff_user_id:
        try:
            # Fetch the staff user object
            staff_user = StaffUser.objects.get(id=staff_user_id)

            # Fetch UserBirthdays related to the staff user
            user_birthdays = UserBirthdays.objects.filter(staff_username=staff_user.username)
            for birthday in user_birthdays:
                users = TelegramUsers.objects.get(telegram_id=birthday.telegram_id)
                user_images = UserBirthdayImages.objects.filter(user_birthday_id=birthday.birthday_id)
                all_birthday_data.append({'user': users, 'user_images': user_images, 'birthday': birthday})
            # Prepare data for rendering the profile template
            staff_user_data = {
                'username': staff_user.username,
                'password': staff_user.password,  # Normally, you would not send the password to the template
            }

            all_birthday_data.reverse()

            return render(request, 'profile.html',
                          {'user_data': staff_user_data, 'all_birthday_data': all_birthday_data})
        except StaffUser.DoesNotExist:
            return HttpResponse("Staff user profile does not exist")
    else:
        return redirect('login')


def update_staff_username(request, birthday_id):
    if request.method == 'POST':
        # Get the UserBirthdays instance
        birthday = get_object_or_404(UserBirthdays, pk=birthday_id)

        # Get the new staff username from the form data
        new_staff_username = request.POST.get('staff_username')

        # Get or create the StaffUser instance corresponding to the staff username
        staff_user, _ = StaffUser.objects.get_or_create(username=new_staff_username)

        # Assign the StaffUser instance to the staff_username field of the UserBirthdays instance
        birthday.staff_username = staff_user

        # Save the changes
        birthday.save()

        messages.success(request, 'Staff username updated successfully')

        # Redirect the user to another page
        return HttpResponse("Staff username updated successfully")

    else:
        # Handle GET requests if needed
        return JsonResponse({'error': 'Invalid request method'})
