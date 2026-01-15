# src/core/signals.py

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from audit.services import log_event
from .models import Patient


def _entity(obj) -> str:
    return f"{obj._meta.app_label}.{obj.__class__.__name__}"


@receiver(pre_save, sender=Patient)
def patient_pre_save(sender, instance: Patient, **kwargs):
    if not instance.pk:
        instance._audit_before = None
        instance._audit_is_active_before = None
        return

    try:
        old = Patient.objects.get(pk=instance.pk)
        instance._audit_before = old.audit_snapshot()
        instance._audit_is_active_before = old.is_active
    except Patient.DoesNotExist:
        instance._audit_before = None
        instance._audit_is_active_before = None


@receiver(post_save, sender=Patient)
def patient_post_save(sender, instance: Patient, created: bool, **kwargs):
    after = instance.audit_snapshot()
    before = getattr(instance, "_audit_before", None)

    if created:
        log_event(
            action="patient.create",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Paciente criado",
            before=None,
            after=after,
            performed_by=None,  # resolve via middleware
        )
        return

    if before is None:
        return

    # Ativar/desativar
    is_active_before = getattr(instance, "_audit_is_active_before", None)
    if is_active_before is not None and is_active_before != instance.is_active:
        log_event(
            action="patient.deactivate" if instance.is_active is False else "patient.activate",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Paciente desativado" if instance.is_active is False else "Paciente reativado",
            before={"is_active": is_active_before},
            after={"is_active": instance.is_active},
            performed_by=None,
        )

    # Update geral (minimalista)
    if before != after:
        log_event(
            action="patient.update",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Paciente atualizado",
            before=before,
            after=after,
            performed_by=None,
        )


@receiver(pre_delete, sender=Patient)
def patient_pre_delete(sender, instance: Patient, **kwargs):
    raise RuntimeError("Delete físico de Patient é proibido. Use inativação (is_active=False).")

# END src/core/signals.py
