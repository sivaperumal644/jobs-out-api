from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from general.models import District, Profession, State
from user import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "first_name", "phone_number"]
    list_filter = ["is_admin"]
    fieldsets = (
        (None, {"fields": ("user_id", "email", "password", "phone_number")}),
        (
            _("Personal Info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "age",
                    "gender",
                    "profession",
                    "experience",
                    "other_skills",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_superuser", "is_staff", "is_admin")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password", "password2")}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Profession)
