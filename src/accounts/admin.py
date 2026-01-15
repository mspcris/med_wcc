from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin do usuário customizado.
    """

    model = User

    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {"fields": ("email",)}),
        (
            "Permissões do sistema",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "can_access_dashboard",
                    "can_manage_patients",
                    "can_manage_schedule",
                    "can_access_care",
                    "can_access_billing",
                    "can_manage_users",
                )
            },
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)
