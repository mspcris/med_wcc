from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """
    Log de auditoria transversal.
    Um registro por evento relevante do sistema.
    """

    # O que aconteceu
    action = models.CharField(max_length=100)  # ex: "user.deactivate", "patient.create"
    entity = models.CharField(max_length=100)  # ex: "accounts.User", "core.Patient"
    entity_id = models.CharField(max_length=64, blank=True)

    # Contexto
    message = models.TextField(blank=True)

    # Estado (quando fizer sentido)
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)

    # Quem / quando
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )
    performed_at = models.DateTimeField(auto_now_add=True)

    # Ambiente
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["entity", "entity_id"]),
            models.Index(fields=["performed_at"]),
        ]
        ordering = ["-performed_at"]

    def __str__(self):
        return f"{self.performed_at} {self.action} {self.entity}:{self.entity_id}"

