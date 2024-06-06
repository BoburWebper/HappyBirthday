from django.contrib import admin

from config.models import TelegramUsers, UserBirthdays, Advertisement, UserBirthdayImages, Card, StaffUser

# Register your models here.
admin.site.register(TelegramUsers)
admin.site.register(UserBirthdays)
admin.site.register(Advertisement)
admin.site.register(UserBirthdayImages)
admin.site.register(Card)


class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)


admin.site.register(StaffUser, StaffUserAdmin)
