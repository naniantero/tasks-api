from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('credits')}),
    )  # type: ignore


admin.site.register(User, UserAdmin)
