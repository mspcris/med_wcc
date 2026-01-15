# src/billing/apps.py
from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billing"

    def ready(self):
        # se no futuro existir billing/signals.py, pode importar aqui também
        # from . import signals  # noqa: F401

        from .delete_guards import register_billing_delete_guards

        register_billing_delete_guards()

# END src/billing/apps.py