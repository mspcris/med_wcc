# src/scheduling/apps.py
from django.apps import AppConfig


class SchedulingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scheduling"

    def ready(self):
        # from . import signals  # noqa: F401
        from .delete_guards import register_scheduling_delete_guards

        register_scheduling_delete_guards()
