from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "is_active",
        "created_at",
    )
    search_fields = ("full_name", "document", "user__username", "user__email")
    list_filter = ("is_active",)
