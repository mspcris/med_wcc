# src/audit/services.py
from django.utils import timezone

from .middleware import get_current_request, get_client_ip, get_current_user
from .models import AuditLog


def log_event(
    *,
    action: str,
    entity: str,
    entity_id: str = "",
    message: str = "",
    before=None,
    after=None,
    performed_by=None,
):
    request = get_current_request()

    ip_address = None
    user_agent = ""

    if request is not None:
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:1000]

    # prioridade:
    # 1) performed_by explícito (quando você passar manualmente)
    # 2) user do request (resolvido via middleware)
    if performed_by is None:
        performed_by = get_current_user()

    AuditLog.objects.create(
        action=action,
        entity=entity,
        entity_id=str(entity_id or ""),
        message=message,
        before=before,
        after=after,
        performed_by=performed_by,
        performed_at=timezone.now(),  # ok manter explícito
        ip_address=ip_address,
        user_agent=user_agent,
    )
# Fim do arquivo src/audit/services.py