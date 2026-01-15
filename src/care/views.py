from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def care_home(request):
    return HttpResponse("Care (placeholder)")
