from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from ninja import Router, Schema
from ninja.errors import HttpError
from ninja.security import django_auth

from cart.services import CartService
from checkout.repositories import OrderRepository
from checkout.services import CheckoutService

router = Router(tags=["Checkout"], auth=django_auth)

_cart_service = CartService()
_checkout_service = CheckoutService()
_order_repo = OrderRepository()


class CheckoutIn(Schema):
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    address_line_1: str
    address_line_2: str = ""
    city: str
    state: str
    postal_code: str
    country: str
    notes: str = ""


class OrderItemOut(Schema):
    id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal


class OrderOut(Schema):
    id: UUID
    status: str
    full_name: str
    email: str
    phone: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    postal_code: str
    country: str
    subtotal: Decimal
    shipping_cost: Decimal
    total: Decimal
    notes: str
    created_at: datetime
    items: List[OrderItemOut]


def _serialize_order(order) -> dict:
    return {
        "id": order.id,
        "status": order.status,
        "full_name": order.full_name,
        "email": order.email,
        "phone": order.phone,
        "address_line_1": order.address_line_1,
        "address_line_2": order.address_line_2,
        "city": order.city,
        "state": order.state,
        "postal_code": order.postal_code,
        "country": order.country,
        "subtotal": order.subtotal,
        "shipping_cost": order.shipping_cost,
        "total": order.total,
        "notes": order.notes,
        "created_at": order.created_at,
        "items": list(order.items.all()),
    }


@router.post("/", response=OrderOut)
def place_order(request, payload: CheckoutIn):
    cart = _cart_service.get_or_create_cart(request)
    order = _checkout_service.place_order(cart, request.user, payload.model_dump())
    return _serialize_order(order)


@router.get("/orders/", response=List[OrderOut])
def list_orders(request):
    orders = _order_repo.get_by_user(request.user)
    return [_serialize_order(o) for o in orders]


@router.get("/orders/{order_id}/", response=OrderOut)
def get_order(request, order_id: UUID):
    order = _order_repo.get_by_id(order_id)
    if order is None or order.user_id != request.user.pk:
        raise HttpError(404, "Order not found")
    return _serialize_order(order)
