# src/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    """
    Usuário principal do sistema.

    - Controle de acesso por funcionalidade (flags)
    - Auditoria completa de ciclo de vida
    - Soft delete (nunca apagar fisicamente)
    """

    # =========================
    # Identidade básica
    # =========================
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    # =========================
    # Flags de acesso (FUNCIONALIDADES)
    # =========================
    can_access_dashboard = models.BooleanField(default=True)
    can_manage_patients = models.BooleanField(default=False)
    can_manage_schedule = models.BooleanField(default=False)
    can_access_care = models.BooleanField(default=False)
    can_access_billing = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)

    # =========================
    # Auditoria de ciclo de vida
    # =========================
    is_deleted = models.BooleanField(default=False)

    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users_deactivated",
    )

    reactivated_at = models.DateTimeField(null=True, blank=True)
    reactivated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users_reactivated",
    )

    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users_deleted",
    )

    # =========================
    # Auditoria técnica
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def audit_snapshot(self) -> dict:
        """
        Estado mínimo auditável do usuário.
        Mantém simples e focado (sem expor senha).
        """
        return {
            "email": self.email,
            "is_active": self.is_active,
            "can_access_dashboard": self.can_access_dashboard,
            "can_manage_patients": self.can_manage_patients,
            "can_manage_schedule": self.can_manage_schedule,
            "can_access_care": self.can_access_care,
            "can_access_billing": self.can_access_billing,
            "can_manage_users": self.can_manage_users,
        }

    def delete(self, using=None, keep_parents=False):
        # Bloqueia obj.delete()
        raise RuntimeError("User não pode ser apagado. Use desativação (is_active=False) ou soft_delete().")

    def soft_delete(self, performed_by=None):
        """
        Delete lógico (nunca físico).
        """
        if self.is_deleted:
            return

        self.is_deleted = True
        self.is_active = False

        if self.deleted_at is None:
            self.deleted_at = timezone.now()
        if performed_by and self.deleted_by_id is None:
            self.deleted_by = performed_by

        self.save(update_fields=["is_deleted", "is_active", "deleted_at", "deleted_by"])

# END src/accounts/models.py
