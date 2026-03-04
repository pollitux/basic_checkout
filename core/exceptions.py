"""
core/exceptions.py

Custom exceptions for the checkout system.
Following SRP: each exception has a specific, single purpose.
"""


class CartException(Exception):
    """Base exception for cart-related errors."""
    pass


class CartItemNotFoundError(CartException):
    """Raised when a cart item is not found."""
    pass


class InsufficientStockError(CartException):
    """Raised when requested quantity exceeds available stock."""

    def __init__(self, product_name: str, available: int):
        self.product_name = product_name
        self.available = available
        super().__init__(
            f"Insufficient stock for '{product_name}'. "
            f"Available: {available}"
        )


class CheckoutException(Exception):
    """Base exception for checkout-related errors."""
    pass


class EmptyCartError(CheckoutException):
    """Raised when attempting to checkout with an empty cart."""
    pass


class OrderCreationError(CheckoutException):
    """Raised when order creation fails."""
    pass


class PaymentException(Exception):
    """Base exception for payment-related errors."""
    pass


class PaymentDeclinedError(PaymentException):
    """Raised when a payment is declined."""
    pass
