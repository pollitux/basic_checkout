"""
checkout/views.py

Checkout views.
ALL checkout URLs are protected with LoginRequiredMixin (SRP for auth).
Business logic is fully delegated to CheckoutService.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from cart.services import CartService
from checkout.forms import CheckoutForm
from checkout.models import Order
from checkout.repositories import OrderRepository
from checkout.services import CheckoutService
from core.exceptions import EmptyCartError, OrderCreationError


class CheckoutView(LoginRequiredMixin, View):
    """
    Checkout form page.

    LoginRequiredMixin ensures unauthenticated users are redirected
    to the login page before they can access checkout (URL protection).
    """

    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cart_service = CartService()
        self._checkout_service = CheckoutService()

    def get(self, request):
        cart = self._cart_service.get_or_create_cart(request)
        if cart.is_empty:
            messages.warning(request, "Your cart is empty.")
            return redirect("cart:detail")

        form = CheckoutForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )
        return render(
            request,
            "checkout/checkout.html",
            {"form": form, "cart": cart},
        )

    def post(self, request):
        """
        Checkout form.
        """
        cart = self._cart_service.get_or_create_cart(request)
        if cart.is_empty:
            messages.warning(request, "Your cart is empty.")
            return redirect("cart:detail")

        form = CheckoutForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "checkout/checkout.html",
                {"form": form, "cart": cart},
            )

        try:
            order = self._checkout_service.place_order(
                cart=cart,
                user=request.user,
                shipping_data=form.get_shipping_data(),
            )
            messages.success(
                request,
                f"Order #{str(order.pk)[:8].upper()} placed successfully!",
            )
            return redirect("checkout:confirmation", order_id=order.pk)

        except EmptyCartError as exc:
            messages.error(request, str(exc))
            return redirect("cart:detail")

        except OrderCreationError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                "checkout/checkout.html",
                {"form": form, "cart": cart},
            )


class OrderConfirmationView(LoginRequiredMixin, View):
    """
    Order confirmation page shown after a successful checkout.

    Protected: only the order's owner can view their confirmation.
    """

    login_url = "/accounts/login/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._order_repo = OrderRepository()

    def get(self, request, order_id):
        """
        Order confirmation page.
        """
        order = get_object_or_404(
            Order,
            pk=order_id,
            user=request.user,  # Object-level permission: owner only.
        )
        return render(
            request,
            "checkout/order_confirmation.html",
            {"order": order},
        )


class OrderHistoryView(LoginRequiredMixin, View):
    """
    List of all orders placed by the current user.

    Protected: LoginRequiredMixin + queryset filtered by user (no leakage).
    """

    login_url = "/accounts/login/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._order_repo = OrderRepository()

    def get(self, request):
        """
        Order history page.
        """
        orders = self._order_repo.get_by_user(request.user)
        return render(
            request,
            "checkout/order_history.html",
            {"orders": orders},
        )


class OrderDetailView(LoginRequiredMixin, View):
    """
    Detail view for a specific historical order.

    Protected: only the order owner can view it (object-level permission).
    """

    login_url = "/accounts/login/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, order_id):
        """
        Order detail page.
        """
        order = get_object_or_404(
            Order,
            pk=order_id,
            user=request.user,
        )
        return render(
            request,
            "checkout/order_detail.html",
            {"order": order},
        )
