from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def billing_home(request):
    return HttpResponse("Billing (placeholder)")
# Additional billing-related views can be added here in the future.