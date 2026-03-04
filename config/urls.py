"""
config/urls.py

Root URL configuration.
URL protection summary:
  - /products/   → public (anyone can browse)
  - /cart/       → public (guests can add items)
  - /checkout/   → protected (LoginRequiredMixin at view level)
  - /accounts/   → django-allauth (login, logout, signup)
  - /admin/      → Django admin (staff only)
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def root_redirect(request):
    return redirect("products:list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("products/", include("products.urls", namespace="products")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("checkout/", include("checkout.urls", namespace="checkout")),
    path("", root_redirect, name="root"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
