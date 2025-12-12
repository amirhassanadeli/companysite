from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    ordering = ('email',)
    list_display = ('email', 'phone', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('phone',)}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('زمان‌ها', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('email', 'phone')
