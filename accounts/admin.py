from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Permission

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("追加情報", {"fields": ("employee_id", "department")}),
    )
    list_display = ('username', 'employee_id', 'department', 'is_staff', 'is_superuser')
    search_fields = ('username', 'employee_id', 'department')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission_level', 'created_at')
    search_fields = ('user__username', 'permission_level')
    list_filter = ('permission_level',)
    ordering = ('-created_at',)