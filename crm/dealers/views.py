from typing import TYPE_CHECKING, cast
from django.forms import ModelChoiceField
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Dealer, Vehicle, VehicleService

if TYPE_CHECKING:
    from accounts.models import User  # SOLO para typing


# =========================
# DEALERS
# =========================

class DealerListView(LoginRequiredMixin, ListView):
    model = Dealer
    template_name = "dealers/dealer_list.html"
    context_object_name = "dealers"


class DealerCreateView(LoginRequiredMixin, CreateView):
    model = Dealer
    fields = [
        "name",
        "rut",
        "email",
        "phone",
        "whatsapp",
        "default_margin_percentage",
    ]
    template_name = "dealers/dealer_form.html"
    success_url = reverse_lazy("dealers:list")


class DealerUpdateView(LoginRequiredMixin, UpdateView):
    model = Dealer
    fields = [
        "name",
        "rut",
        "email",
        "phone",
        "whatsapp",
        "default_margin_percentage",
    ]
    template_name = "dealers/dealer_form.html"
    success_url = reverse_lazy("dealers:list")


class DealerDeleteView(LoginRequiredMixin, DeleteView):
    model = Dealer
    template_name = "dealers/dealer_confirm_delete.html"
    success_url = reverse_lazy("dealers:list")


# =========================
# VEHICLES
# =========================

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "dealers/vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        user = cast("User", self.request.user)
        return Vehicle.objects.filter(dealer=user.dealer)


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    fields = [
        "brand",
        "model",
        "year",
        "ownership_type",
        "purchase_price",
        "currency",
    ]
    template_name = "dealers/vehicle_form.html"
    success_url = reverse_lazy("dealers:vehicle_list")

    def form_valid(self, form):
        user = cast("User", self.request.user)
        form.instance.dealer = user.dealer
        return super().form_valid(form)


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    fields = [
        "brand",
        "model",
        "year",
        "ownership_type",
        "purchase_price",
        "currency",
    ]
    template_name = "dealers/vehicle_form.html"
    success_url = reverse_lazy("dealers:vehicle_list")

    def get_queryset(self):
        user = cast("User", self.request.user)
        return Vehicle.objects.filter(dealer=user.dealer)


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = "dealers/vehicle_confirm_delete.html"
    success_url = reverse_lazy("dealers:vehicle_list")

    def get_queryset(self):
        user = cast("User", self.request.user)
        return Vehicle.objects.filter(dealer=user.dealer)

class VehicleServiceListView(LoginRequiredMixin, ListView):
    model = VehicleService
    template_name = "dealers/vehicle_service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        user = cast("User", self.request.user)
        return VehicleService.objects.filter(
            vehicle__dealer=user.dealer
        ).select_related("vehicle")


class VehicleServiceCreateView(LoginRequiredMixin, CreateView):
    model = VehicleService
    fields = [
        "vehicle",
        "description",
        "amount",
        "payer",
        "service_date",
    ]
    template_name = "dealers/vehicle_service_form.html"
    success_url = reverse_lazy("dealers:vehicle_service_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = cast("User", self.request.user)

        vehicle_field = cast(
            ModelChoiceField,
            form.fields["vehicle"]
        )
        vehicle_field.queryset = Vehicle.objects.filter(
            dealer=user.dealer
        )

        return form

class VehicleServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = VehicleService
    fields = [
        "vehicle",
        "description",
        "amount",
        "payer",
        "service_date",
    ]
    template_name = "dealers/vehicle_service_form.html"
    success_url = reverse_lazy("dealers:vehicle_service_list")

    def get_queryset(self):
        user = cast("User", self.request.user)
        return VehicleService.objects.filter(
            vehicle__dealer=user.dealer
        )


class VehicleServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = VehicleService
    template_name = "dealers/vehicle_service_confirm_delete.html"
    success_url = reverse_lazy("dealers:vehicle_service_list")

    def get_queryset(self):
        user = cast("User", self.request.user)
        return VehicleService.objects.filter(
            vehicle__dealer=user.dealer
        )