"""
products/repositories.py

Product repository: isolates all product-related DB queries (SRP + DIP).
Views and services depend on this abstraction, not on the ORM directly.
"""
from typing import List, Optional

from core.repositories import BaseRepository
from products.models import Category, Product


class ProductRepository(BaseRepository[Product]):
    """Concrete repository for Product persistence operations."""

    def get_by_id(self, pk) -> Optional[Product]:
        """
        Retrieve a product by its ID.
        """
        try:
            return Product.objects.select_related("category").get(
                pk=pk, is_active=True
            )
        except Product.DoesNotExist:
            return None

    def get_by_slug(self, slug: str) -> Optional[Product]:
        """
        Retrieve a product by its slug.
        """
        try:
            return Product.objects.select_related("category").get(
                slug=slug, is_active=True
            )
        except Product.DoesNotExist:
            return None

    def get_all(self) -> List[Product]:
        """
        Retrieve all products.
        """
        return list(
            Product.objects.select_related("category").filter(is_active=True)
        )

    def get_available(self) -> List[Product]:
        """Return only products with stock > 0."""
        return list(
            Product.objects.select_related("category").filter(
                is_active=True, stock__gt=0
            )
        )

    def get_available_by_category(self, category: Optional[Category]) -> List[Product]:
        """Return available products filtered by category."""
        qs = Product.objects.select_related("category").filter(
            is_active=True, stock__gt=0
        )
        if category:
            qs = qs.filter(category=category)
        return list(qs)

    def save(self, entity: Product) -> Product:
        """
        Save a new product.
        """
        entity.save()
        return entity

    def delete(self, entity: Product) -> None:
        """
        Delete a product.
        """
        entity.delete()


class CategoryRepository(BaseRepository[Category]):
    """Concrete repository for Category persistence operations."""

    def get_by_id(self, pk) -> Optional[Category]:
        """
        Retrieve a category by its ID.
        """
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get_by_slug(self, slug: str) -> Optional[Category]:
        """
        Retrieve a category by its slug.
        """
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None

    def get_all(self) -> List[Category]:
        """
        Retrieve all categories.
        """
        return list(Category.objects.all())

    def save(self, entity: Category) -> Category:
        """
        Save a new category.
        """
        entity.save()
        return entity

    def delete(self, entity: Category) -> None:
        """
        Delete a category.
        """
        entity.delete()
