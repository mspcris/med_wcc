from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("performed_at", "action", "entity", "entity_id", "performed_by", "ip_address")
    list_filter = ("action", "entity")
    search_fields = ("action", "entity", "entity_id", "message", "performed_by__username", "performed_by__email")
    readonly_fields = (
        "action",
        "entity",
        "entity_id",
        "message",
        "before",
        "after",
        "performed_by",
        "performed_at",
        "ip_address",
        "user_agent",
    )
