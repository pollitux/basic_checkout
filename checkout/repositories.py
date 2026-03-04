"""
checkout/repositories.py

Order repository: isolates all Order-related DB queries (SRP + DIP).
"""
from typing import List, Optional

from core.repositories import BaseRepository
from checkout.models import Order, OrderItem


class OrderRepository(BaseRepository[Order]):
    """Handles Order persistence operations."""

    def get_by_id(self, pk) -> Optional[Order]:
        """
        Get an Order by ID.
        """
        try:
            return Order.objects.prefetch_related("items").get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get_all(self) -> List[Order]:
        """
        Get all Orders.
        """
        return list(Order.objects.prefetch_related("items").all())

    def get_by_user(self, user) -> List[Order]:
        """
        Get an Order by user.
        """
        return list(
            Order.objects.prefetch_related("items")
            .filter(user=user)
            .order_by("-created_at")
        )

    def save(self, entity: Order) -> Order:
        """
        Save an Order.
        """
        entity.save()
        return entity

    def delete(self, entity: Order) -> None:
        """
        Delete an Order.
        """
        entity.delete()


class OrderItemRepository(BaseRepository[OrderItem]):
    """Handles OrderItem persistence operations."""

    def get_by_id(self, pk) -> Optional[OrderItem]:
        """
        Get an OrderItem by its ID.
        """
        try:
            return OrderItem.objects.select_related("order", "product").get(pk=pk)
        except OrderItem.DoesNotExist:
            return None

    def get_all(self) -> List[OrderItem]:
        """
        Get all OrderItems.
        """
        return list(OrderItem.objects.all())

    def save(self, entity: OrderItem) -> OrderItem:
        """
        Save an OrderItem by its ID.
        """
        entity.save()
        return entity

    def delete(self, entity: OrderItem) -> None:
        """
        Delete an OrderItem by its ID.
        """
        entity.delete()
