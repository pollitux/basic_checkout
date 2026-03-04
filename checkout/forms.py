"""
checkout/forms.py

Checkout form: collects shipping and contact information.
Widget attrs use Tailwind utility classes for consistent styling.
"""
from django import forms

INPUT_CLASS = (
    "w-full bg-black border border-[#2a2a2a] text-white "
    "font-mono text-sm px-4 py-3 focus:outline-none "
    "focus:border-[#e8ff4a] placeholder-gray-700 transition-colors"
)
TEXTAREA_CLASS = INPUT_CLASS + " resize-none"


class CheckoutForm(forms.Form):
    """Shipping address and contact form for checkout."""

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "John", "class": INPUT_CLASS}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Doe", "class": INPUT_CLASS}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": INPUT_CLASS}),
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "+1 555 000 0000", "class": INPUT_CLASS}),
    )
    address_line_1 = forms.CharField(
        max_length=255,
        label="Address line 1",
        widget=forms.TextInput(attrs={"placeholder": "123 Main St", "class": INPUT_CLASS}),
    )
    address_line_2 = forms.CharField(
        max_length=255,
        required=False,
        label="Address line 2",
        widget=forms.TextInput(attrs={"placeholder": "Apt 4B", "class": INPUT_CLASS}),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Sahuayo", "class": INPUT_CLASS}),
    )
    state = forms.CharField(
        max_length=100,
        label="State / Province",
        widget=forms.TextInput(attrs={"placeholder": "MICH", "class": INPUT_CLASS}),
    )
    postal_code = forms.CharField(
        max_length=20,
        label="Postal code",
        widget=forms.TextInput(attrs={"placeholder": "10001", "class": INPUT_CLASS}),
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "México", "class": INPUT_CLASS}),
    )
    notes = forms.CharField(
        required=False,
        label="Order notes",
        widget=forms.Textarea(attrs={
            "placeholder": "Special instructions (optional)",
            "rows": 3,
            "class": TEXTAREA_CLASS,
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
