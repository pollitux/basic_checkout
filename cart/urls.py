"""
cart/urls.py

Cart URL patterns.
All cart mutations (add/remove/update) are POST-only — enforced by the
View class. GET-only detail view is accessible to all (guests included).
"""
from django.urls import path

from cart.views import (
    AddToCartView,
    CartDetailView,
    RemoveFromCartView,
    UpdateCartView,
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("add/<uuid:product_id>/", AddToCartView.as_view(), name="add"),
    path("remove/<uuid:item_id>/", RemoveFromCartView.as_view(), name="remove"),
    path("update/<uuid:item_id>/", UpdateCartView.as_view(), name="update"),
]
