"""
core/models.py

Abstract base models following OCP (Open/Closed Principle).
Open for extension, closed for modification.
"""
import uuid

from django.db import models


class TimestampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    created_at and updated_at fields.

    Follows OCP: subclasses extend without modifying this base.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(TimestampedModel):
    """
    Abstract base model using UUID as primary key.
    Provides unpredictable IDs for security (hides record counts).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
