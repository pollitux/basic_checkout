"""
cart/repositories.py

Cart and CartItem repositories: pure data-access layer (SRP + DIP).
"""
from typing import Optional

from django.contrib.auth import get_user_model

from cart.models import Cart, CartItem
from core.repositories import BaseRepository
from products.models import Product

User = get_user_model()


class CartRepository(BaseRepository[Cart]):
    """Handles Cart persistence operations."""

    def get_by_id(self, pk) -> Optional[Cart]:
        """
        Retrieve a cart by its ID.
        """
        try:
            return Cart.objects.prefetch_related(
                "items__product"
            ).get(pk=pk)
        except Cart.DoesNotExist:
            return None

    def get_by_user(self, user: User) -> Optional[Cart]:
        """
        Retrieve a cart by its user.
        """
        try:
            return Cart.objects.prefetch_related(
                "items__product"
            ).get(user=user)
        except Cart.DoesNotExist:
            return None

    def get_by_session(self, session_key: str) -> Optional[Cart]:
        """
        Retrieve a cart by its session key.
        """
        try:
            return Cart.objects.prefetch_related(
                "items__product"
            ).get(session_key=session_key)
        except Cart.DoesNotExist:
            return None

    def get_all(self):
        """
        Retrieve all carts.
        """
        return list(Cart.objects.all())

    def save(self, entity: Cart) -> Cart:
        """
        Save a new cart.
        """
        entity.save()
        return entity

    def delete(self, entity: Cart) -> None:
        """
        Delete a cart.
        """
        entity.delete()

    def get_or_create_for_user(self, user: User) -> Cart:
        """
        Retrieve a cart by its user.
        """
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get_or_create_for_session(self, session_key: str) -> Cart:
        """
        Retrieve a cart by its session.
        """
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart


class CartItemRepository(BaseRepository[CartItem]):
    """Handles CartItem persistence operations."""

    def get_by_id(self, pk) -> Optional[CartItem]:
        try:
            return CartItem.objects.select_related(
                "product", "cart"
            ).get(pk=pk)
        except CartItem.DoesNotExist:
            return None

    def get_all(self):
        """
        Retrieve all carts.
        """
        return list(CartItem.objects.all())

    def get_by_cart_and_product(
            self, cart: Cart, product: Product
    ) -> Optional[CartItem]:
        """
        Retrieve a cart item by its cart and product.
        """
        try:
            return CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            return None

    def save(self, entity: CartItem) -> CartItem:
        """
        Save a new cart item.
        """
        entity.save()
        return entity

    def delete(self, entity: CartItem) -> None:
        """
        Delete a cart item.
        """
        entity.delete()
