"""
checkout/urls.py

Checkout URL patterns.
All views are additionally protected at the view layer via LoginRequiredMixin.
"""
from django.urls import path

from checkout.views import (
    CheckoutView,
    OrderConfirmationView,
    OrderDetailView,
    OrderHistoryView,
)

app_name = "checkout"

urlpatterns = [
    path("", CheckoutView.as_view(), name="checkout"),
    path(
        "confirmation/<uuid:order_id>/",
        OrderConfirmationView.as_view(),
        name="confirmation",
    ),
    path("orders/", OrderHistoryView.as_view(), name="order_history"),
    path(
        "orders/<uuid:order_id>/",
        OrderDetailView.as_view(),
        name="order_detail",
    ),
]
