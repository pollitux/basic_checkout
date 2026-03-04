from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin class
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin class
    """
    list_display = (
        "show_image", "name", "price", "stock"
    )
    list_editable = ("name", "price")
    search_fields = ("name", "slug")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}

    def show_image(self, obj):
        """

        :param obj:
        :return:
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image}" width="50" height="50" />')
        return mark_safe(
            f'<img src="https://dummyimage.com/600x400/ffffff/75756a.jpg&text=not+image" width="50" height="50" />'
        )

    show_image.short_description = 'Image'
