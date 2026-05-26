from django.contrib import admin
from django.utils.safestring import mark_safe

from contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Contact admin class.
    """
    list_display = ['show_photo', 'full_name', 'email', 'phone', 'is_blocked']
    list_editable = ('email', 'phone',)
    search_fields = ['full_name', 'email', 'phone']
    list_filter = ['segment', 'is_blocked']

    def show_photo(self, obj):
        """

        :param obj:
        :return:
        """
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo}" width="100" height="100" />')
        return mark_safe(
            f'<img src="https://dummyimage.com/600x400/ffffff/75756a.jpg&text=not+image" width="50" height="50" />'
        )

    show_photo.short_description = 'photo'
