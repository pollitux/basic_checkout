from uuid import UUID

from contacts.models import Contact
from contacts.repositories import ContactRepository


class ContactService:
    def __init__(self):
        self._repo = ContactRepository()

    def list_contacts(self, segment: str | None = None) -> list[Contact]:
        if segment:
            return self._repo.get_by_segment(segment)
        return self._repo.get_all()

    def get_contact(self, contact_id: UUID) -> Contact | None:
        return self._repo.get_by_id(contact_id)

    def create_contact(self, data: dict) -> Contact:
        contact = Contact(**data)
        return self._repo.save(contact)

    def update_contact(self, contact_id: UUID, data: dict) -> Contact | None:
        contact = self._repo.get_by_id(contact_id)
        if contact is None:
            return None
        for key, value in data.items():
            setattr(contact, key, value)
        return self._repo.save(contact)

    def delete_contact(self, contact_id: UUID) -> bool:
        contact = self._repo.get_by_id(contact_id)
        if contact is None:
            return False
        self._repo.delete(contact)
        return True
