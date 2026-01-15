# src/scheduling/delete_guards.py
from django.apps import apps as django_apps
from django.db.models.signals import pre_delete


def _prevent_physical_delete(sender, instance, **kwargs):
    raise RuntimeError(
        f"Delete físico de {sender.__name__} é proibido. Use inativação (is_active=False) ou soft_delete()."
    )


def register_scheduling_delete_guards():
    app_config = django_apps.get_app_config("scheduling")

    for model in app_config.get_models():
        pre_delete.connect(
            _prevent_physical_delete,
            sender=model,
            dispatch_uid=f"scheduling.no_physical_delete.{model._meta.label_lower}",
        )
