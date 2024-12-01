from django.contrib import admin
from .models import CustomUser

# Register your models here.

class Users(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'invite_code', 'activated_invite_code')


admin.site.register(CustomUser)