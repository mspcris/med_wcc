# src/core/apps.py
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from . import signals  # noqa: F401
        from .delete_guards import register_core_delete_guards

        register_core_delete_guards()

# END src/core/apps.py
