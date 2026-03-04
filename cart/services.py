"""
cart/services.py

CartService: encapsulates all cart business logic (SRP).
Views delegate to this service; they never touch the ORM directly.
This follows the Facade pattern, providing a simple API to a complex subsystem.
"""
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest

from cart.models import Cart, CartItem
from cart.repositories import CartItemRepository, CartRepository
from core.exceptions import (
    CartItemNotFoundError,
    InsufficientStockError,
)
from products.repositories import ProductRepository


class CartService:
    """
    Manages all cart operations.

    Depends on abstractions (repositories), not concrete implementations.
    This satisfies the Dependency Inversion Principle.
    """

    def __init__(self):
        self._cart_repo = CartRepository()
        self._item_repo = CartItemRepository()
        self._product_repo = ProductRepository()

    # Cart resolution
    def get_or_create_cart(self, request: HttpRequest) -> Cart:
        """
        Resolve the cart for the current request.

        Strategy:
        - Authenticated user → use user-linked cart.
        - Anonymous user     → use session-linked cart.
        """
        if request.user.is_authenticated:
            return self._cart_repo.get_or_create_for_user(request.user)

        if not request.session.session_key:
            request.session.create()
        return self._cart_repo.get_or_create_for_session(
            request.session.session_key
        )

    # Mutations

    def add_item(
            self, request: HttpRequest, product_id: str, quantity: int = 1
    ) -> CartItem:
        """
        Add a product to the cart or increment its quantity.

        Raises:
            InsufficientStockError: if stock cannot satisfy the request.
        """
        product = self._product_repo.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Product {product_id} not found.")

        cart = self.get_or_create_cart(request)
        existing_item = self._item_repo.get_by_cart_and_product(cart, product)
        new_quantity = (existing_item.quantity if existing_item else 0) + quantity

        if not product.has_sufficient_stock(new_quantity):
            raise InsufficientStockError(product.name, product.stock)

        if existing_item:
            existing_item.quantity = new_quantity
            return self._item_repo.save(existing_item)

        item = CartItem(cart=cart, product=product, quantity=quantity)
        return self._item_repo.save(item)

    def remove_item(self, request: HttpRequest, item_id: str) -> None:
        """
        Remove a specific item from the cart.

        Raises:
            CartItemNotFoundError: if the item does not belong to this cart.
        """
        cart = self.get_or_create_cart(request)
        item = self._item_repo.get_by_id(item_id)

        if item is None or item.cart_id != cart.id:
            raise CartItemNotFoundError(
                f"Cart item {item_id} not found in current cart."
            )

        self._item_repo.delete(item)

    def update_quantity(
            self, request: HttpRequest, item_id: str, quantity: int
    ) -> CartItem:
        """
        Set a cart item's quantity.

        Raises:
            CartItemNotFoundError: if the item does not belong to this cart.
            InsufficientStockError: if quantity exceeds available stock.
            ValueError: if quantity is less than 1.
        """
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")

        cart = self.get_or_create_cart(request)
        item = self._item_repo.get_by_id(item_id)

        if item is None or item.cart_id != cart.id:
            raise CartItemNotFoundError(
                f"Cart item {item_id} not found in current cart."
            )

        if not item.product.has_sufficient_stock(quantity):
            raise InsufficientStockError(item.product.name, item.product.stock)

        item.quantity = quantity
        return self._item_repo.save(item)

    def clear_cart(self, cart: Cart) -> None:
        """Remove all items from a cart."""
        cart.items.all().delete()

    def merge_session_cart(
            self, session_key: str, user: AbstractBaseUser
    ) -> None:
        """
        Merge an anonymous session cart into the authenticated user cart.
        Called on login (Observer/signal pattern — see apps.py).
        """
        session_cart = self._cart_repo.get_by_session(session_key)
        if session_cart is None:
            return

        user_cart = self._cart_repo.get_or_create_for_user(user)

        for item in session_cart.items.select_related("product").all():
            existing = self._item_repo.get_by_cart_and_product(
                user_cart, item.product
            )
            if existing:
                merged_qty = min(
                    existing.quantity + item.quantity, item.product.stock
                )
                existing.quantity = merged_qty
                self._item_repo.save(existing)
            else:
                item.pk = None  # Detach from session cart
                item.cart = user_cart
                self._item_repo.save(item)

        self._cart_repo.delete(session_cart)
