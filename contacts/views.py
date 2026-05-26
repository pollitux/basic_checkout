"""
contacts/views.py

Contact views: thin controllers that delegate to repositories (SRP).
"""
from django.shortcuts import render
from django.views import View

from contacts.models import Contact
from contacts.repositories import ContactRepository


class ContactListView(View):
    """Displays the contacts agenda, optionally filtered by segment."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._contact_repo = ContactRepository()

    def get(self, request):
        active_segment = request.GET.get("segment")

        if active_segment:
            contacts = self._contact_repo.get_by_segment(active_segment)
        else:
            contacts = self._contact_repo.get_all()

        return render(
            request,
            "contacts/contact_list.html",
            {
                "contacts": contacts,
                "active_segment": active_segment,
                "segments": Contact.segment.field.choices,
            },
        )
