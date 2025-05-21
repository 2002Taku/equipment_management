from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Permission

admin.site.register(CustomUser, UserAdmin)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission_level', 'created_at')
    search_fields = ('user__username', 'permission_level')
    list_filter = ('permission_level',)
    ordering = ('-created_at',)