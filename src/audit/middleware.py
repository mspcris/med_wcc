# src/audit/middleware.py
import threading

_thread_locals = threading.local()


def set_current_request(request):
    _thread_locals.request = request


def get_current_request():
    return getattr(_thread_locals, "request", None)


def set_current_user(user):
    _thread_locals.user = user


def get_current_user():
    return getattr(_thread_locals, "user", None)


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuditRequestMiddleware:
    """
    Armazena o request e o usuário atual em thread local.
    Permite que signals/services consigam pegar:
    - usuário logado
    - ip
    - user_agent
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)

        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            set_current_user(user)
        else:
            set_current_user(None)

        return self.get_response(request)
# END src/audit/middleware.py
