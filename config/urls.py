from django.urls import path
from .views import home, login_view, profile_view, update_staff_username

urlpatterns = [
    path('', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('home/', home, name='home'),
    path('update_staff_username/<int:birthday_id>/', update_staff_username, name='update_staff_username'),
]
