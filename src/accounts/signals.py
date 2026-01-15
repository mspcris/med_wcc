# src/accounts/signals.py

from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from audit.services import log_event
from .models import User


def _entity(user: User) -> str:
    return f"{user._meta.app_label}.{user.__class__.__name__}"


FLAG_KEYS = [
    "can_access_dashboard",
    "can_manage_patients",
    "can_manage_schedule",
    "can_access_care",
    "can_access_billing",
    "can_manage_users",
]


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance: User, **kwargs):
    """
    Guarda snapshot antes de salvar, para comparar no post_save.
    Também guarda is_active/is_deleted anterior para auditoria de ciclo de vida.
    """
    if not instance.pk:
        instance._audit_before = None
        instance._audit_is_active_before = None
        instance._audit_is_deleted_before = None
        return

    try:
        old = User.objects.get(pk=instance.pk)
        instance._audit_before = old.audit_snapshot()
        instance._audit_is_active_before = old.is_active
        instance._audit_is_deleted_before = old.is_deleted
    except User.DoesNotExist:
        instance._audit_before = None
        instance._audit_is_active_before = None
        instance._audit_is_deleted_before = None


@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created: bool, **kwargs):
    """
    Registra eventos:
    - user.create
    - user.update_flags (quando flags mudarem)
    - user.deactivate / user.activate (quando is_active mudar)
    - user.soft_delete (quando is_deleted mudar)
    E também preenche os campos:
    - deactivated_at / deactivated_by
    - reactivated_at / reactivated_by
    (sem loop infinito: faz update() no banco, não chama save())
    """
    after = instance.audit_snapshot()
    before = getattr(instance, "_audit_before", None)

    is_active_before = getattr(instance, "_audit_is_active_before", None)
    is_deleted_before = getattr(instance, "_audit_is_deleted_before", None)

    if created:
        log_event(
            action="user.create",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Usuário criado",
            before=None,
            after=after,
            performed_by=None,  # audit.services resolve via middleware
        )
        return

    # Se não conseguiu pegar "before", não audita update
    if before is None:
        return

    # =========================================================
    # Ciclo de vida: is_active (ativar/desativar)
    # =========================================================
    if is_active_before is not None and is_active_before != instance.is_active:
        now = timezone.now()

        if instance.is_active is False:
            # Desativar
            def _apply_deactivate_fields():
                # atualiza apenas se estiver vazio (não sobrescreve auditoria)
                updates = {}
                if instance.deactivated_at is None:
                    updates["deactivated_at"] = now
                if instance.deactivated_by_id is None:
                    # audit.services usa middleware para descobrir o user atual;
                    # aqui, seguimos o mesmo mecanismo via performed_by no log.
                    # Para gravar no User, deixamos o performed_by ser resolvido no service
                    # e apenas registramos o evento; se quiser gravar no User também,
                    # precisamos de um getter explícito (já existe no audit.middleware).
                    from audit.middleware import get_current_user  # import local para evitar ciclo
                    cu = get_current_user()
                    if cu is not None:
                        updates["deactivated_by"] = cu

                if updates:
                    User.objects.filter(pk=instance.pk).update(**updates)

            transaction.on_commit(_apply_deactivate_fields)

            log_event(
                action="user.deactivate",
                entity=_entity(instance),
                entity_id=instance.pk,
                message="Usuário desativado",
                before={"is_active": is_active_before},
                after={"is_active": instance.is_active},
                performed_by=None,
            )

        else:
            # Reativar
            def _apply_reactivate_fields():
                updates = {}
                if instance.reactivated_at is None:
                    updates["reactivated_at"] = now
                if instance.reactivated_by_id is None:
                    from audit.middleware import get_current_user  # import local para evitar ciclo
                    cu = get_current_user()
                    if cu is not None:
                        updates["reactivated_by"] = cu

                if updates:
                    User.objects.filter(pk=instance.pk).update(**updates)

            transaction.on_commit(_apply_reactivate_fields)

            log_event(
                action="user.activate",
                entity=_entity(instance),
                entity_id=instance.pk,
                message="Usuário reativado",
                before={"is_active": is_active_before},
                after={"is_active": instance.is_active},
                performed_by=None,
            )

    # =========================================================
    # Flags (permissões)
    # =========================================================
    changed_flags = {k: (before.get(k), after.get(k)) for k in FLAG_KEYS if before.get(k) != after.get(k)}
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

    # =========================================================
    # Soft delete (is_deleted)
    # =========================================================
    if is_deleted_before is not None and is_deleted_before != instance.is_deleted and instance.is_deleted is True:
        now = timezone.now()

        def _apply_deleted_fields():
            updates = {}
            if instance.deleted_at is None:
                updates["deleted_at"] = now
            if instance.deleted_by_id is None:
                from audit.middleware import get_current_user  # import local para evitar ciclo
                cu = get_current_user()
                if cu is not None:
                    updates["deleted_by"] = cu
            # garante inativação junto
            if instance.is_active is True:
                updates["is_active"] = False
                if instance.deactivated_at is None:
                    updates["deactivated_at"] = now
                if instance.deactivated_by_id is None:
                    from audit.middleware import get_current_user
                    cu = get_current_user()
                    if cu is not None:
                        updates["deactivated_by"] = cu

            if updates:
                User.objects.filter(pk=instance.pk).update(**updates)

        transaction.on_commit(_apply_deleted_fields)

        log_event(
            action="user.soft_delete",
            entity=_entity(instance),
            entity_id=instance.pk,
            message="Usuário marcado como deletado (soft delete)",
            before={"is_deleted": is_deleted_before},
            after={"is_deleted": instance.is_deleted},
            performed_by=None,
        )

# END src/accounts/signals.py
