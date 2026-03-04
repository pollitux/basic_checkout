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
        try:
            return Order.objects.prefetch_related("items").get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get_all(self) -> List[Order]:
        return list(Order.objects.prefetch_related("items").all())

    def get_by_user(self, user) -> List[Order]:
        return list(
            Order.objects.prefetch_related("items")
            .filter(user=user)
            .order_by("-created_at")
        )

    def save(self, entity: Order) -> Order:
        entity.save()
        return entity

    def delete(self, entity: Order) -> None:
        entity.delete()


class OrderItemRepository(BaseRepository[OrderItem]):
    """Handles OrderItem persistence operations."""

    def get_by_id(self, pk) -> Optional[OrderItem]:
        try:
            return OrderItem.objects.select_related("order", "product").get(pk=pk)
        except OrderItem.DoesNotExist:
            return None

    def get_all(self) -> List[OrderItem]:
        return list(OrderItem.objects.all())

    def save(self, entity: OrderItem) -> OrderItem:
        entity.save()
        return entity

    def delete(self, entity: OrderItem) -> None:
        entity.delete()
