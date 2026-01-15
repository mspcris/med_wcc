# src/audit/middleware.py
import threading

_thread_locals = threading.local()

def set_current_request(request):
    _thread_locals.request = request

def get_current_request():
    return getattr(_thread_locals, "request", None)

def get_current_user():
    req = get_current_request()
    user = getattr(req, "user", None)
    return user if getattr(user, "is_authenticated", False) else None



def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuditRequestMiddleware:
    """
    Guarda o request atual em thread local.
    Signals/services conseguem capturar:
    - usuário logado
    - ip
    - user_agent
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)
        try:
            return self.get_response(request)
        finally:
            # evita “vazar” request entre requests no mesmo worker/thread
            set_current_request(None)

# END src/audit/middleware.py
