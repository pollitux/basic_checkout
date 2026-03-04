"""
products/models.py

Product catalog models.
Each model class has a single, well-defined responsibility (SRP).
"""
from django.db import models
from django.utils.text import slugify

from core.models import UUIDModel


class Category(UUIDModel):
    """Represents a product category."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(UUIDModel):
    """
    Represents a purchasable product.

    Encapsulates product data and provides business-rule methods
    without leaking persistence logic (SRP).
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self) -> bool:
        """Business rule: product is available if stock > 0."""
        return self.stock > 0

    def has_sufficient_stock(self, quantity: int) -> bool:
        """Check if the requested quantity can be fulfilled."""
        return self.stock >= quantity
