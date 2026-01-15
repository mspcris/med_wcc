from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
