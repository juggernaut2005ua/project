# backend/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'level', 'points', 'created_at']
    list_filter = ['role', 'level', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informacje dodatkowe', {
            'fields': ('role', 'age', 'points', 'level', 'avatar', 'parent_email', 'two_factor_enabled')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informacje dodatkowe', {
            'fields': ('role', 'age', 'parent_email')
        }),
    )