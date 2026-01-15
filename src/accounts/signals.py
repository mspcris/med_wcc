# src/accounts/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from audit.services import log_event
from .models import User


def _entity(user: User) -> str:
    return f"{user._meta.app_label}.{user.__class__.__name__}"


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance: User, **kwargs):
    """
    Guarda snapshot antes de salvar, para comparar no post_save.
    """
    if not instance.pk:
        instance._audit_before = None
        return

    try:
        old = User.objects.get(pk=instance.pk)
        instance._audit_before = old.audit_snapshot()
    except User.DoesNotExist:
        instance._audit_before = None


@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created: bool, **kwargs):
    """
    Registra eventos:
    - user.create
    - user.update_flags (quando flags mudarem)
    - user.deactivate / user.activate (quando is_active mudar)
    """
    after = instance.audit_snapshot()
    before = getattr(instance, "_audit_before", None)

    if created:
        log_event(
            action="user.create",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Usuário criado",
            before=None,
            after=after,
            performed_by=None,  # middleware resolve
        )
        return

    if before is None:
        return

    # Detectar mudança de is_active
    if before.get("is_active") != after.get("is_active"):
        log_event(
            action="user.deactivate" if after["is_active"] is False else "user.activate",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Usuário desativado" if after["is_active"] is False else "Usuário reativado",
            before={"is_active": before.get("is_active")},
            after={"is_active": after.get("is_active")},
            performed_by=None,
        )

    # Detectar mudanças nas flags (qualquer flag mudou)
    flag_keys = [
        "can_access_dashboard",
        "can_manage_patients",
        "can_manage_schedule",
        "can_access_care",
        "can_access_billing",
        "can_manage_users",
    ]

    changed_flags = {k: (before.get(k), after.get(k)) for k in flag_keys if before.get(k) != after.get(k)}

    if changed_flags:
        log_event(
            action="user.update_flags",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Alteração de permissões (flags)",
            before={k: before.get(k) for k in changed_flags.keys()},
            after={k: after.get(k) for k in changed_flags.keys()},
            performed_by=None,
        )
# END src/accounts/signals.py