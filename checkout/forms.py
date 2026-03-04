"""
checkout/forms.py

Checkout form: collects shipping and contact information.
Kept thin — validation logic lives in the form, business logic in the service.
"""
from django import forms


class CheckoutForm(forms.Form):
    """Shipping address and contact form for checkout."""

    # ---- Contact info ----
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "First name", "class": "form-input"}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Last name", "class": "form-input"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email address", "class": "form-input"}),
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Phone (optional)", "class": "form-input"}),
    )

    # ---- Shipping address ----
    address_line_1 = forms.CharField(
        max_length=255,
        label="Address line 1",
        widget=forms.TextInput(attrs={"placeholder": "Street address", "class": "form-input"}),
    )
    address_line_2 = forms.CharField(
        max_length=255,
        required=False,
        label="Address line 2",
        widget=forms.TextInput(attrs={"placeholder": "Apt, suite, etc. (optional)", "class": "form-input"}),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-input"}),
    )
    state = forms.CharField(
        max_length=100,
        label="State / Province",
        widget=forms.TextInput(attrs={"placeholder": "State / Province", "class": "form-input"}),
    )
    postal_code = forms.CharField(
        max_length=20,
        label="Postal code",
        widget=forms.TextInput(attrs={"placeholder": "Postal code", "class": "form-input"}),
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Country", "class": "form-input"}),
    )

    # ---- Order notes ----
    notes = forms.CharField(
        required=False,
        label="Order notes",
        widget=forms.Textarea(attrs={
            "placeholder": "Special instructions for your order (optional)",
            "rows": 3,
            "class": "form-input",
        }),
    )

    def get_shipping_data(self) -> dict:
        """Return only the cleaned shipping/contact fields."""
        fields = [
            "first_name", "last_name", "email", "phone",
            "address_line_1", "address_line_2", "city",
            "state", "postal_code", "country", "notes",
        ]
        return {field: self.cleaned_data[field] for field in fields}
