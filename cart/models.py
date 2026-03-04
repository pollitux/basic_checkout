"""
cart/models.py

Shopping cart models.
Cart is session-based for guests; linked to user when authenticated.
"""
from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import UUIDModel
from products.models import Product


class Cart(UUIDModel):
    """
    Represents a shopping cart.

    A cart belongs to either an authenticated user or an anonymous
    session. It cannot belong to both simultaneously (business rule).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart",
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            # A cart must belong to a user OR a session, never neither.
            models.CheckConstraint(
                check=(
                        models.Q(user__isnull=False)
                        | models.Q(session_key__isnull=False)
                ),
                name="cart_has_owner",
            )
        ]

    def __str__(self) -> str:
        owner = self.user or f"session:{self.session_key}"
        return f"Cart({owner})"

    @property
    def total_price(self) -> Decimal:
        """Aggregate total from all cart items."""
        return sum(item.subtotal for item in self.items.select_related("product").all())

    @property
    def total_items(self) -> int:
        """Total number of individual units in the cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def is_empty(self) -> bool:
        return not self.items.exists()


class CartItem(UUIDModel):
    """
    Represents a single line in a cart.

    Encapsulates the quantity/price relationship for one product (SRP).
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self) -> Decimal:
        """Price of this line: unit price × quantity."""
        return self.product.price * self.quantity
