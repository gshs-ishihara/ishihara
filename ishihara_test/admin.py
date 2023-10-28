from django.contrib import admin
from .models import UserInfo, IshiharaTest, Contact


# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'token', 'uuid', 'submitted_at')
    ordering = ('-submitted_at',)


@admin.register(IshiharaTest)
class IshiharaTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
