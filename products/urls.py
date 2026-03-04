"""
products/urls.py

URL patterns for the product catalog.
"""
from django.urls import path

from products.views import ProductDetailView, ProductListView

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]
