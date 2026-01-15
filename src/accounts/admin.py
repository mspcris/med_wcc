# src/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import Staff
from .models import User


class StaffInline(admin.StackedInline):
    model = Staff
    extra = 0
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin do usuário customizado.
    Regra: usuário NÃO pode ser apagado fisicamente (somente desativado).
    """

    model = User
    inlines = (StaffInline,)

    actions = None  # remove ações em massa (inclui delete_selected)

    def has_delete_permission(self, request, obj=None):
        # Ninguém apaga usuário fisicamente pelo admin
        return False

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
        (_("Informações pessoais"), {"fields": ("email",)}),
        (
            _("Permissões do sistema (flags)"),
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
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
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
# END src/accounts/admin.py
