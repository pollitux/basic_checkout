"""
contacts/repositories.py

Contact repository: isolates all contact-related DB queries (SRP + DIP).
"""
from typing import List, Optional

from core.repositories import BaseRepository
from contacts.models import Contact


class ContactRepository(BaseRepository[Contact]):
    """Concrete repository for Contact persistence operations."""

    def get_by_id(self, pk) -> Optional[Contact]:
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return None

    def get_all(self) -> List[Contact]:
        return list(Contact.objects.all())

    def get_by_segment(self, segment: str) -> List[Contact]:
        return list(Contact.objects.filter(segment=segment))

    def save(self, entity: Contact) -> Contact:
        entity.save()
        return entity

    def delete(self, entity: Contact) -> None:
        entity.delete()
