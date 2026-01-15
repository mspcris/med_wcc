# src/core/apps.py
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # mantém seus signals existentes (audit do Patient, etc.)
        from . import signals  # noqa: F401

        # registra o bloqueio genérico de delete físico do app core
        from ..core.delete_guards import register_core_delete_guards

        register_core_delete_guards()


# END src/core/apps.py
