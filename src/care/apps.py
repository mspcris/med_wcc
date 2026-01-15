# src/care/apps.py
from django.apps import AppConfig


class CareConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "care"

    def ready(self):
        # from . import signals  # noqa: F401
        from .delete_guards import register_care_delete_guards

        register_care_delete_guards()
