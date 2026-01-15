from django.urls import path
from .views import billing_home

urlpatterns = [
    path("", billing_home, name="billing_home"),
]
