from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .services import log_event


@receiver(user_logged_in)
def audit_login(sender, request, user, **kwargs):
    log_event(
        action="auth.login",
        entity=f"{user._meta.app_label}.{user.__class__.__name__}",
        entity_id=user.pk,
        message="Login realizado",
        performed_by=user,
    )


@receiver(user_logged_out)
def audit_logout(sender, request, user, **kwargs):
    if user is None:
        return
    log_event(
        action="auth.logout",
        entity=f"{user._meta.app_label}.{user.__class__.__name__}",
        entity_id=user.pk,
        message="Logout realizado",
        performed_by=user,
    )


@receiver(user_login_failed)
def audit_login_failed(sender, credentials, request, **kwargs):
    username = credentials.get("username") or credentials.get("email") or ""
    log_event(
        action="auth.login_failed",
        entity="accounts.User",
        entity_id="",
        message=f"Tentativa de login falhou: {username}",
        performed_by=None,
    )

