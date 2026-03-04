"""
products/views.py

Product views: thin controllers that delegate to repositories (SRP).
Views only handle HTTP request/response — no business logic here.
"""
from django.shortcuts import get_object_or_404, render
from django.views import View

from products.repositories import CategoryRepository, ProductRepository


class ProductListView(View):
    """Displays the product catalog, optionally filtered by category slug."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._product_repo = ProductRepository()
        self._category_repo = CategoryRepository()

    def get(self, request):
        """
        Return a list of products.
        """
        category_slug = request.GET.get("category")
        active_category = None

        if category_slug:
            active_category = self._category_repo.get_by_slug(category_slug)
            products = self._product_repo.get_available_by_category(active_category)
        else:
            products = self._product_repo.get_available()

        return render(
            request,
            "products/product_list.html",
            {
                "products": products,
                "active_category": active_category,
            },
        )


class ProductDetailView(View):
    """Displays a single product detail page."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._product_repo = ProductRepository()

    def get(self, request, slug: str):
        product = self._product_repo.get_by_slug(slug)
        if product is None:
            from django.http import Http404
            raise Http404("Product not found.")
        return render(
            request,
            "products/product_detail.html",
            {"product": product},
        )
