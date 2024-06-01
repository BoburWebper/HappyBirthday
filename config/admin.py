from django.contrib import admin

from config.models import Users, UserBirthdays, Advertisement,UserBirthdayImages, Card

# Register your models here.
admin.site.register(Users)
admin.site.register(UserBirthdays)
admin.site.register(Advertisement)
admin.site.register(UserBirthdayImages)
admin.site.register(Card)