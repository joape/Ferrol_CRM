from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Dealer


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

