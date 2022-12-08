from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class MyUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'role',
                    'bio', 'first_name', 'last_name')

    ADDITIONAL_USER_FIELDS = (
        (None, {'fields': ('role', 'bio',)}),
    )

    fieldsets = ADDITIONAL_USER_FIELDS + UserAdmin.fieldsets


admin.site.register(User, MyUserAdmin)
