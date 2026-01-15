from django.conf import settings
from django.db import models


class Patient(models.Model):
    """
    Paciente do sistema.

    - Vinculado a um usuário (login)
    - Contém apenas dados clínicos/administrativos
    - Totalmente auditável
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="patient_profile",
    )

    # Dados básicos
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    document = models.CharField(max_length=50, blank=True)

    # Auditoria de ciclo de vida
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="patients_created",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="patients_updated",
    )

    def __str__(self):
        return self.full_name
