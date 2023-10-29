from django.contrib import admin
from .models import UserInfo, IshiharaTest, Contact


# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'share_count', 'submitted_at')
    readonly_fields = ('token', 'uuid', 'submitted_at')
    ordering = ('-submitted_at',)


@admin.register(IshiharaTest)
class IshiharaTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'submitted_at')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
