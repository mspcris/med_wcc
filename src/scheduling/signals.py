from django.apps import apps
from django.db.models.signals import pre_delete


def _prevent_physical_delete(sender, instance, **kwargs):
    raise RuntimeError(
        f"Delete físico de {sender.__name__} é proibido. Use inativação (is_active=False) ou soft_delete()."
    )


def register_delete_guards(app_label: str):
    app_config = apps.get_app_config(app_label)

    for model in app_config.get_models():
        pre_delete.connect(
            _prevent_physical_delete,
            sender=model,
            dispatch_uid=f"{app_label}.no_physical_delete.{model.__name__}",
        )


register_delete_guards("scheduling")
