# src/audit/signals_auth.py

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .services import log_event


def _entity_user():
    return "accounts.User"


@receiver(user_logged_in)
def audit_user_logged_in(sender, request, user, **kwargs):
    log_event(
        action="auth.login",
        entity=_entity_user(),
        entity_id=user.pk,
        message="Login realizado",
        before=None,
        after={"user_id": user.pk, "username": getattr(user, "username", "")},
        performed_by=user,  # aqui pode ser o próprio
    )


@receiver(user_logged_out)
def audit_user_logged_out(sender, request, user, **kwargs):
    # user pode ser None em alguns cenários
    uid = getattr(user, "pk", "")
    log_event(
        action="auth.logout",
        entity=_entity_user(),
        entity_id=uid,
        message="Logout realizado",
        before=None,
        after={"user_id": uid, "username": getattr(user, "username", "")},
        performed_by=user,
    )


@receiver(user_login_failed)
def audit_user_login_failed(sender, credentials, request, **kwargs):
    # credentials costuma ter "username" (depende do backend)
    username = ""
    try:
        username = credentials.get("username") or credentials.get("email") or ""
    except Exception:
        username = ""

    log_event(
        action="auth.login_failed",
        entity=_entity_user(),
        entity_id="",
        message="Falha de login",
        before=None,
        after={"username": username},
        performed_by=None,
    )
