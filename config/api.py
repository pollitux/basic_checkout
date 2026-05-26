from ninja import NinjaAPI

from core.exceptions import (
    CartItemNotFoundError,
    EmptyCartError,
    InsufficientStockError,
    OrderCreationError,
)

api = NinjaAPI(
    title="Basic Checkout API",
    version="1.0.0",
    description="REST API for the basic checkout project.",
)


@api.exception_handler(InsufficientStockError)
def handle_insufficient_stock(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=400)


@api.exception_handler(CartItemNotFoundError)
def handle_cart_item_not_found(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=404)


@api.exception_handler(EmptyCartError)
def handle_empty_cart(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=400)


@api.exception_handler(OrderCreationError)
def handle_order_creation(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=400)


@api.exception_handler(ValueError)
def handle_value_error(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=400)


from cart.api import router as cart_router
from checkout.api import router as checkout_router
from contacts.api import router as contacts_router
from core.api import router as auth_router
from products.api import router as products_router

api.add_router("/auth/", auth_router)
api.add_router("/products/", products_router)
api.add_router("/cart/", cart_router)
api.add_router("/checkout/", checkout_router)
api.add_router("/contacts/", contacts_router)
