from django.contrib import admin
from .models import Dealer, Vehicle, VehicleService


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "rut", "email", "is_active")
    search_fields = ("name", "rut", "email")
    list_filter = ("is_active",)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "model",
        "year",
        "dealer",
        "ownership_type",
        "purchase_price",
        "currency",
    )
    list_filter = ("dealer", "ownership_type", "currency")
    search_fields = ("brand", "model")

@admin.register(VehicleService)
class VehicleServiceAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle",
        "description",
        "amount",
        "payer",
        "service_date",
    )
    list_filter = ("payer", "service_date")
    search_fields = ("description",)