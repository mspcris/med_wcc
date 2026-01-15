from django.utils import timezone

from .models import AuditLog
from .middleware import get_current_request, get_client_ip

from typing import Optional
from django.contrib.auth import get_user_model
from .middleware import get_current_request, get_client_ip, get_current_user



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
        performed_by = get_current_user()


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

_user_local = {"user": None}

def set_current_user(user):
    _user_local["user"] = user

def get_current_user() -> Optional[object]:
    return _user_local.get("user")
