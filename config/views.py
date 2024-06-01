from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import UserBirthdays, UserBirthdayImages, Users


def home(request):
    today = datetime.now().date()
    birthdays = UserBirthdays.objects.all()
    birthdays_with_users = []

    for birthday in birthdays:
        user = Users.objects.get(telegram_id=birthday.telegram_id)
        user_images = UserBirthdayImages.objects.filter(user_birthday_id=birthday.birthday_id)
        birthdays_with_users.append({'birthday': birthday, 'user': user, 'images': user_images})
        birthdays_with_users.reverse()

    return render(request, 'index.html', {'birthdays_with_users': birthdays_with_users})



