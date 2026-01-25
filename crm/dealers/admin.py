from django.contrib import admin
from .models import Dealer


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "rut", "email", "is_active")
    search_fields = ("name", "rut", "email")
    list_filter = ("is_active",)