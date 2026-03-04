"""
products/context_processors.py

Injects the category list into every template context automatically.
This follows SRP: categories in the navbar are a cross-cutting concern,
not the responsibility of any single view.
"""
from products.repositories import CategoryRepository


def categories(request) -> dict:
    """Make all categories available in every template as `categories`."""
    repo = CategoryRepository()
    return {"categories": repo.get_all()}
