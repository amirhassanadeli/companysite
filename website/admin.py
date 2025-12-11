from django.contrib import admin

from .models import Service, Project, TeamMember, Contact, JobRequest


# ==============================
# Service
# ==============================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)
    fieldsets = (
        ("اطلاعات سرویس", {
            "fields": ("title", "description", "icon", "category")
        }),
        ("تنظیمات نمایش", {
            "fields": ("order", "is_active")
        }),
    )


# ==============================
# Project
# ==============================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "order", "is_featured")
    list_editable = ("order", "is_featured")
    search_fields = ("title", "description")
    list_filter = ("is_featured", "created_at")
    filter_horizontal = ("technologies",)
    ordering = ("order", "-is_featured", "-created_at")
    fieldsets = (
        ("اطلاعات پروژه", {
            "fields": ("title", "short_description", "description", "image")
        }),
        ("لینک‌ها", {
            "fields": ("demo_url", "github_url")
        }),
        ("مشخصات تکنولوژی", {
            "fields": ("technologies",)
        }),
        ("تنظیمات نمایش", {
            "fields": ("order", "is_featured")
        }),
    )


# ==============================
# Team Member
# ==============================
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "telegram", "github", "linkedin", "order")
    list_editable = ("order",)
    search_fields = ("user__email", "user__username", "position")
    list_filter = ("position",)
    ordering = ("order",)
    fieldsets = (
        ("کاربر", {
            "fields": ("user", "position")
        }),
        ("اطلاعات کارمند", {
            "fields": ("bio", "image")
        }),
        ("شبکه‌های اجتماعی", {
            "fields": ("github", "linkedin", "telegram")
        }),
        ("تنظیمات نمایش", {
            "fields": ("order",)
        }),
    )


# ==============================
# Contact Messages
# ==============================
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "phone", "message", "ip")
    readonly_fields = ("created_at", "ip")
    ordering = ("is_read", "-created_at")
    list_editable = ("is_read",)

    fieldsets = (
        ("اطلاعات مخاطب", {
            "fields": ("name", "phone", "email")
        }),
        ("متن پیام", {
            "fields": ("message",)
        }),
        ("سیستمی", {
            "fields": ("ip", "created_at", "is_read", "is_deleted"),
            "classes": ("collapse",)
        }),
    )


# ==============================
# Job Requests (درخواست همکاری)
# ==============================
@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "get_field_display", "created_at", "is_reviewed")
    list_filter = ("field", "is_reviewed", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at", "ip")
    ordering = ("-created_at",)
    list_editable = ("is_reviewed",)

    fieldsets = (
        ("مشخصات متقاضی", {
            "fields": ("name", "email", "phone", "user")
        }),
        ("اطلاعات همکاری", {
            "fields": ("field", "message")
        }),
        ("سیستمی", {
            "fields": ("ip", "created_at", "is_reviewed", "is_deleted"),
            "classes": ("collapse",)
        }),
    )

    def get_field_display(self, obj):
        return obj.get_field_display()

    get_field_display.short_description = "حوزه همکاری"
