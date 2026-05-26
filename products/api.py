from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from ninja import Router, Schema
from ninja.errors import HttpError

from products.repositories import CategoryRepository, ProductRepository

router = Router(tags=["Products"])

_product_repo = ProductRepository()
_category_repo = CategoryRepository()


class CategoryOut(Schema):
    id: UUID
    name: str
    slug: str
    description: str


class ProductOut(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    price: Decimal
    stock: int
    is_active: bool
    image: Optional[str]
    category: Optional[CategoryOut]


@router.get("/", response=List[ProductOut])
def list_products(request, category: Optional[str] = None):
    if category:
        cat = _category_repo.get_by_slug(category)
        if cat is None:
            raise HttpError(404, "Category not found")
        return _product_repo.get_available_by_category(cat)
    return _product_repo.get_available()


@router.get("/categories/", response=List[CategoryOut])
def list_categories(request):
    return _category_repo.get_all()


@router.get("/{slug}/", response=ProductOut)
def get_product(request, slug: str):
    product = _product_repo.get_by_slug(slug)
    if product is None:
        raise HttpError(404, "Product not found")
    return product
