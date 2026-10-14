from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "reference", "bundle_name", "amount_fcfa", "payment_method", "status")
    list_filter = ("payment_method", "status", "created_at")
    search_fields = ("reference", "bundle_name")
    readonly_fields = ("reference", "created_at", "bundle_code", "bundle_name", "data_volume", "amount_fcfa", "payment_method", "status")
    ordering = ("-created_at",)
