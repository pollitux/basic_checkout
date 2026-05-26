from decimal import Decimal
from typing import List
from uuid import UUID

from ninja import Router, Schema
from ninja.errors import HttpError

from cart.services import CartService

router = Router(tags=["Cart"])

_cart_service = CartService()


class ProductSimpleOut(Schema):
    id: UUID
    name: str
    slug: str
    price: Decimal


class CartItemOut(Schema):
    id: UUID
    product: ProductSimpleOut
    quantity: int
    subtotal: Decimal


class CartOut(Schema):
    id: UUID
    total_price: Decimal
    total_items: int
    items: List[CartItemOut]


class AddToCartIn(Schema):
    quantity: int = 1


class UpdateCartIn(Schema):
    quantity: int


def _serialize_item(item) -> dict:
    return {
        "id": item.id,
        "product": item.product,
        "quantity": item.quantity,
        "subtotal": item.subtotal,
    }


@router.get("/", response=CartOut)
def get_cart(request):
    cart = _cart_service.get_or_create_cart(request)
    return {
        "id": cart.id,
        "total_price": cart.total_price,
        "total_items": cart.total_items,
        "items": [
            _serialize_item(item)
            for item in cart.items.select_related("product").all()
        ],
    }


@router.post("/add/{product_id}/", response=CartItemOut)
def add_to_cart(request, product_id: UUID, payload: AddToCartIn):
    item = _cart_service.add_item(request, str(product_id), payload.quantity)
    return _serialize_item(item)


@router.delete("/remove/{item_id}/", response={204: None})
def remove_from_cart(request, item_id: UUID):
    _cart_service.remove_item(request, str(item_id))
    return 204, None


@router.patch("/update/{item_id}/", response=CartItemOut)
def update_cart_item(request, item_id: UUID, payload: UpdateCartIn):
    item = _cart_service.update_quantity(request, str(item_id), payload.quantity)
    return _serialize_item(item)
