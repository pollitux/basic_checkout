"""
cart/views.py

Cart views: HTTP layer only. All logic delegated to CartService (SRP).
"""
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from cart.services import CartService
from core.exceptions import CartItemNotFoundError, InsufficientStockError


class CartDetailView(View):
    """Display the current user's cart."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cart_service = CartService()

    def get(self, request):
        cart = self._cart_service.get_or_create_cart(request)
        return render(request, "cart/cart_detail.html", {"cart": cart})


class AddToCartView(View):
    """Add a product to the cart (supports AJAX)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cart_service = CartService()

    def post(self, request, product_id: str):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity < 1:
                raise ValueError("Quantity must be positive.")

            item = self._cart_service.add_item(request, product_id, quantity)
            cart = self._cart_service.get_or_create_cart(request)

            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "message": f"'{item.product.name}' added to cart.",
                    "cart_total_items": cart.total_items,
                })

            messages.success(request, f"'{item.product.name}' added to your cart.")

        except (InsufficientStockError, ValueError, Exception) as exc:
            if is_ajax:
                return JsonResponse({"success": False, "message": str(exc)}, status=400)
            messages.error(request, str(exc))

        return redirect(request.META.get("HTTP_REFERER", "products:list"))


class RemoveFromCartView(View):
    """Remove a cart item."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cart_service = CartService()

    def post(self, request, item_id: str):
        try:
            self._cart_service.remove_item(request, item_id)
            messages.success(request, "Item removed from your cart.")
        except CartItemNotFoundError as exc:
            messages.error(request, str(exc))
        return redirect("cart:detail")


class UpdateCartView(View):
    """Update the quantity of a cart item."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cart_service = CartService()

    def post(self, request, item_id: str):
        try:
            quantity = int(request.POST.get("quantity", 1))
            self._cart_service.update_quantity(request, item_id, quantity)
            messages.success(request, "Cart updated.")
        except (CartItemNotFoundError, InsufficientStockError, ValueError) as exc:
            messages.error(request, str(exc))
        return redirect("cart:detail")
