from django.urls import path
from .views import scheduling_home

urlpatterns = [
    path("", scheduling_home, name="scheduling_home"),
]
