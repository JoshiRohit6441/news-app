from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


class AdminModel(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "username", "password", "verification_otp"
            ),
        }),
        ("User information", {
            "fields": (
                "email", "first_name", "last_name", "profile_pic"
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_admin", "is_active", "groups", "user_permissions"
            ),
        }),
        ("Date", {
            "fields": ["last_login"]
        }),
    )

    list_filter = ('is_admin', "is_active")
    list_display = ("id", "username", "email",
                    "is_admin", "is_active", "profile_image", "created_at")

    def profile_image(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.profile_pic.url))
        else:
            return None


admin.site.register(User, AdminModel)
