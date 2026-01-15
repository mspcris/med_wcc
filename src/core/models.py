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


# src/core/models.py
from django.conf import settings
from django.db import models


class Staff(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RECEPTION = "RECEPTION", "Recepção"
        NURSE = "NURSE", "Enfermagem"
        DOCTOR = "DOCTOR", "Médico"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff",
    )

    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=20, choices=Role.choices)

    # Só para médico (role=DOCTOR)
    crm = models.CharField(max_length=32, blank=True, default="")
    specialty = models.CharField(max_length=80, blank=True, default="")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def audit_snapshot(self) -> dict:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "role": self.role,
            "crm": self.crm,
            "specialty": self.specialty,
            "is_active": self.is_active,
        }

    def delete(self, using=None, keep_parents=False):
        raise RuntimeError("Staff não pode ser apagado fisicamente. Use is_active=False.")

# END src/core/models.py
