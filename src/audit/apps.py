# src/audit/apps.py
from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "audit"

    def ready(self):
        # Importa signals somente quando o Django já carregou os apps
        from . import signals_auth  # noqa: F401
        # Se você tiver outros signals do audit, importe aqui também:
        # from . import signals  # noqa: F401
