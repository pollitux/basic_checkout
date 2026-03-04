"""
checkout/services.py

CheckoutService: orchestrates order creation from a cart (SRP, OCP, DIP).

Design patterns used:
- Strategy Pattern  : payment processing (swappable strategies)
- Factory Pattern   : order + order-items creation
- Facade Pattern    : simple interface over a complex multi-step process
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from django.db import models, transaction

from cart.models import Cart
from cart.services import CartService
from checkout.models import Order, OrderItem
from checkout.repositories import OrderItemRepository, OrderRepository
from core.exceptions import EmptyCartError, OrderCreationError
from products.models import Product


# Strategy Pattern: Payment Processing
@dataclass
class PaymentResult:
    """Value object returned by every payment strategy."""

    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None


class PaymentStrategy(ABC):
    """
    Abstract payment strategy.
    OCP: add new strategies without modifying existing ones.
    """

    @abstractmethod
    def process(self, amount: Decimal, order: Order) -> PaymentResult:
        """
        Process payment strategy.
        """
        raise NotImplementedError


class DummyPaymentStrategy(PaymentStrategy):
    """
    Development/demo payment strategy — always succeeds.
    Replace with Stripe, PayPal, etc. in production.
    """

    def process(self, amount: Decimal, order: Order) -> PaymentResult:
        import uuid
        return PaymentResult(
            success=True,
            transaction_id=str(uuid.uuid4()),
        )


class StripePaymentStrategy(PaymentStrategy):
    """
    Placeholder for Stripe integration.
    Demonstrates OCP: extend without modifying CheckoutService.
    """

    def __init__(self, api_key: str):
        self._api_key = api_key

    def process(self, amount: Decimal, order: Order) -> PaymentResult:
        # TODO: integrate stripe.PaymentIntent.create(...)
        raise NotImplementedError("Stripe integration not configured.")


# Factory Pattern: Order creation
class OrderFactory:
    """
    Creates Order and OrderItem instances from a Cart.
    Encapsulates construction logic so CheckoutService stays clean (SRP).
    """

    SHIPPING_COST = Decimal("5.00")

    def build(self, cart: Cart, user, shipping_data: dict) -> Order:
        """Instantiate an Order (not yet saved) from cart + shipping data."""
        subtotal = cart.total_price
        total = subtotal + self.SHIPPING_COST

        return Order(
            user=user,
            subtotal=subtotal,
            shipping_cost=self.SHIPPING_COST,
            total=total,
            **shipping_data,
        )

    def build_items(self, order: Order, cart: Cart) -> list:
        """Instantiate OrderItems snapshotting current prices."""
        items = []
        for cart_item in cart.items.select_related("product").all():
            items.append(
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    unit_price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )
            )
        return items


# Checkout Service (Facade)
class CheckoutService:
    """
    Orchestrates the full checkout flow.
    Depends on abstractions (DIP): payment strategy and repositories
    are injected, not hardcoded.
    """

    def __init__(
            self,
            payment_strategy: Optional[PaymentStrategy] = None,
            order_repo: Optional[OrderRepository] = None,
            order_item_repo: Optional[OrderItemRepository] = None,
            order_factory: Optional[OrderFactory] = None,
            cart_service: Optional[CartService] = None,
    ):
        self._payment = payment_strategy or DummyPaymentStrategy()
        self._order_repo = order_repo or OrderRepository()
        self._item_repo = order_item_repo or OrderItemRepository()
        self._factory = order_factory or OrderFactory()
        self._cart_service = cart_service or CartService()

    @transaction.atomic
    def place_order(self, cart: Cart, user, shipping_data: dict) -> Order:
        """
        Execute the full checkout flow atomically:
        1. Validate cart is not empty.
        2. Build order + items via factory.
        3. Save order and items.
        4. Decrement product stock (with select_for_update).
        5. Process payment via strategy.
        6. Confirm order status.
        7. Clear cart.

        Raises:
            EmptyCartError: if the cart has no items.
            OrderCreationError: if payment fails.
        """
        if cart.is_empty:
            raise EmptyCartError("Cannot checkout with an empty cart.")

        # Step 1 — Build and persist order (factory)
        order = self._factory.build(cart, user, shipping_data)
        self._order_repo.save(order)

        items = self._factory.build_items(order, cart)
        for item in items:
            self._item_repo.save(item)
            self._decrement_stock(item)

        # Step 2 — Process payment (strategy)
        result = self._payment.process(order.total, order)
        if not result.success:
            raise OrderCreationError(
                f"Payment failed: {result.error_message}"
            )

        # Step 3 — Confirm and clear
        order.status = Order.Status.CONFIRMED
        self._order_repo.save(order)
        self._cart_service.clear_cart(cart)

        return order

    @staticmethod
    def _decrement_stock(item: OrderItem) -> None:
        """Safely decrement product stock using select_for_update."""
        (
            Product.objects.select_for_update()
            .filter(pk=item.product_id)
            .update(stock=models.F("stock") - item.quantity)
        )
