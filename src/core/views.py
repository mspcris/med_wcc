from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from dataclasses import dataclass

@login_required
def home(request):
    user = request.user
    flags = [
        ("Dashboard", user.can_access_dashboard),
        ("Pacientes", user.can_manage_patients),
        ("Agenda", user.can_manage_schedule),
        ("Clínico", user.can_access_care),
        ("Financeiro", user.can_access_billing),
        ("Usuários", user.can_manage_users),
    ]
    return render(request, "core/home.html", {"flags": flags})

@dataclass(frozen=True)
class MenuItem:
    label: str
    url: str
    enabled: bool


@login_required
def home(request):
    u = request.user

    menu = [
        MenuItem("Dashboard", "/", u.can_access_dashboard),
        MenuItem("Pacientes", "/admin/core/patient/", u.can_manage_patients),
        MenuItem("Agenda", "/scheduling/", u.can_manage_schedule),
        MenuItem("Prontuário", "/care/", u.can_access_care),
        MenuItem("Financeiro", "/billing/", u.can_access_billing),
        MenuItem("Usuários (Admin)", "/admin/accounts/user/", u.can_manage_users),
    ]

    # Mostra só o que o usuário pode ver
    visible_menu = [m for m in menu if m.enabled]

    return render(
        request,
        "core/home.html",
        {"menu": visible_menu},
    )
