from django.urls import path
from .views import (
    DealerListView,
    DealerCreateView,
    DealerUpdateView,
    DealerDeleteView,
)

app_name = "dealers"

urlpatterns = [
    path("", DealerListView.as_view(), name="list"),
    path("new/", DealerCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", DealerUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", DealerDeleteView.as_view(), name="delete"),
]
