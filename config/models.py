from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User


# Create your models here.

class TelegramUsers(models.Model):
    user_id = models.AutoField(primary_key=True)
    telegram_id = models.TextField(unique=True, null=False)
    firstname = models.CharField(max_length=100, null=False)
    lastname = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.telegram_id


class StaffUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class UserBirthdays(models.Model):
    birthday_id = models.AutoField(primary_key=True)
    telegram_id = models.ForeignKey(TelegramUsers, to_field='telegram_id', on_delete=models.SET_NULL, null=True)
    staff_username = models.ForeignKey(StaffUser, to_field='username', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=300, null=False)
    age = models.IntegerField(null=False)
    friends = models.TextField(null=False)  # Kimlar nomidan
    close_friends = models.TextField(null=False)  # Aynan kim nomidan
    wishlist = models.TextField(null=True, blank=True, default=None)  # Tilaklar
    phone_number = models.CharField(max_length=13, null=False)
    birthday = models.DateField()
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}; Birthday: {self.birthday} Payment Status: {self.payment_status}"


class UserBirthdayImages(models.Model):
    user_birthday = models.ForeignKey(UserBirthdays, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/birthday/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.user_birthday}"


class Advertisement(models.Model):
    text = models.TextField(null=False)
    image = models.ImageField(upload_to='media/advertising/image', null=True, blank=True)
    video = models.FileField(upload_to='media/advertising/video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.text


class Card(models.Model):
    cardInfo = models.TextField(null=True)
