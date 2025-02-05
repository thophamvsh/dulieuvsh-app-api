from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime  # Chuyển đổi múi giờ

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'formatted_last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Thời gian đăng nhập'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

    def formatted_last_login(self, obj):
        """Hiển thị thời gian đăng nhập theo múi giờ Việt Nam."""
        if obj.last_login:
            return localtime(obj.last_login).strftime('%d/%m/%Y %H:%M:%S')  # Format ngày giờ
        return '-'

    formatted_last_login.short_description = "Lần đăng nhập cuối"

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

admin.site.register(models.User, UserAdmin)
