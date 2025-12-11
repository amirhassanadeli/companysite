from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # ستون‌هایی که در لیست کاربران نمایش داده می‌شود
    list_display = ("email", "username", "is_staff", "is_superuser", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)

    # نمایش فیلدها داخل صفحه ویرایش User
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("دسترسی‌ها", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("زمان‌ها", {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ("last_login", "date_joined")

    # فرم ساخت کاربر جدید در admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_superuser", "is_active")
        }),
    )
