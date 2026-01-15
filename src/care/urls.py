from django.urls import path
from .views import care_home

urlpatterns = [
    path("", care_home, name="care_home"),
]
