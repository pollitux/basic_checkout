from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from ninja import Router, Schema
from ninja.errors import HttpError
from ninja.security import django_auth

from contacts.services import ContactService

router = Router(tags=["Contacts"], auth=django_auth)

_contact_service = ContactService()

VALID_SEGMENTS = {"family", "work", "friends", "other", "favourite"}


class ContactIn(Schema):
    full_name: str
    email: str
    phone: str
    segment: str = "other"
    is_blocked: bool = False
    birthday: Optional[date] = None
    photo: Optional[str] = None


class ContactOut(Schema):
    id: UUID
    full_name: str
    email: str
    phone: str
    segment: str
    is_blocked: bool
    birthday: Optional[date]
    photo: Optional[str]
    created_at: datetime
    updated_at: datetime


@router.get("/", response=List[ContactOut])
def list_contacts(request, segment: Optional[str] = None):
    if segment and segment not in VALID_SEGMENTS:
        raise HttpError(400, f"Invalid segment. Choices: {', '.join(VALID_SEGMENTS)}")
    return _contact_service.list_contacts(segment)


@router.post("/", response=ContactOut)
def create_contact(request, payload: ContactIn):
    if payload.segment not in VALID_SEGMENTS:
        raise HttpError(400, f"Invalid segment. Choices: {', '.join(VALID_SEGMENTS)}")
    return _contact_service.create_contact(payload.model_dump())


@router.get("/{contact_id}/", response=ContactOut)
def get_contact(request, contact_id: UUID):
    contact = _contact_service.get_contact(contact_id)
    if contact is None:
        raise HttpError(404, "Contact not found")
    return contact


@router.put("/{contact_id}/", response=ContactOut)
def update_contact(request, contact_id: UUID, payload: ContactIn):
    if payload.segment not in VALID_SEGMENTS:
        raise HttpError(400, f"Invalid segment. Choices: {', '.join(VALID_SEGMENTS)}")
    contact = _contact_service.update_contact(contact_id, payload.model_dump())
    if contact is None:
        raise HttpError(404, "Contact not found")
    return contact


@router.delete("/{contact_id}/", response={204: None})
def delete_contact(request, contact_id: UUID):
    deleted = _contact_service.delete_contact(contact_id)
    if not deleted:
        raise HttpError(404, "Contact not found")
    return 204, None
