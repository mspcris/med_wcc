from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


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
