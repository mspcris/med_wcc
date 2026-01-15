# src/core/models.py

from django.conf import settings
from django.db import models


class Patient(models.Model):
    """
    Paciente do sistema.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # não deixa apagar User se existir Patient
        related_name="patient",
    )

    full_name = models.CharField(max_length=200)
    document = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def audit_snapshot(self) -> dict:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "document": self.document,
            "phone": self.phone,
            "is_active": self.is_active,
        }

    def delete(self, using=None, keep_parents=False):
        raise RuntimeError("Patient não pode ser apagado fisicamente. Use inativação (is_active=False).")

# END src/core/models.py
