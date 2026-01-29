from django.urls import path
from .views import (
    DealerListView,
    DealerCreateView,
    DealerUpdateView,
    DealerDeleteView,
    VehicleListView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
    VehicleServiceListView,
    VehicleServiceCreateView,
    VehicleServiceUpdateView,
    VehicleServiceDeleteView,
)

app_name = "dealers"

urlpatterns = [
    path("", DealerListView.as_view(), name="list"),
    path("new/", DealerCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", DealerUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", DealerDeleteView.as_view(), name="delete"),

    path("vehicles/", VehicleListView.as_view(), name="vehicle_list"),
    path("vehicles/new/", VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicles/<int:pk>/edit/", VehicleUpdateView.as_view(), name="vehicle_update"),
    path("vehicles/<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle_delete"),

    path("services/", VehicleServiceListView.as_view(), name="vehicle_service_list"),
    path("services/new/", VehicleServiceCreateView.as_view(), name="vehicle_service_create"),
    path("services/<int:pk>/edit/", VehicleServiceUpdateView.as_view(), name="vehicle_service_update"),
    path("services/<int:pk>/delete/", VehicleServiceDeleteView.as_view(), name="vehicle_service_delete"),
    
]
