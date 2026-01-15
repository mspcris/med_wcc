# src/core/admin.py
from django.contrib import admin
from .models import Patient, Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "user", "is_active", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("full_name", "user__username", "user__email", "crm", "document", "specialty")
    actions = None  # remove delete_selected

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False
# END
