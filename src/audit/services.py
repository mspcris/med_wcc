from django.utils import timezone

from .models import AuditLog
from .middleware import get_current_request, get_client_ip


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
    req_user = None

    if request is not None:
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:1000]
        req_user = getattr(request, "user", None)

    if performed_by is None:
        if req_user is not None and getattr(req_user, "is_authenticated", False):
            performed_by = req_user

    AuditLog.objects.create(
        action=action,
        entity=entity,
        entity_id=str(entity_id or ""),
        message=message,
        before=before,
        after=after,
        performed_by=performed_by,
        performed_at=timezone.now(),
        ip_address=ip_address,
        user_agent=user_agent,
    )
