from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
