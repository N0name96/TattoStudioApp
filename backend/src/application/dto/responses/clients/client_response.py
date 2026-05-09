"""Response DTOs for the clients module.

Contains Pydantic models for serializing client data.
These DTOs are used by the API layer to format responses.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ClientResponse(BaseModel):
    """Response DTO for client data.

    Used to return client information to the API client.
    Maps from domain entity to a serializable format.

    Attributes:
        id: Unique identifier for the client.
        full_name: Client's full name.
        email: Contact email address.
        phone: Phone number.
        birth_date: Client's birth date.
        allergies: Known allergies.
        medical_conditions: Known medical conditions.
        source: How the client discovered the studio.
        image_rights: Set of image rights granted.
        notes: Internal notes.
        is_active: Whether the client record is active.
        created_at: When the client record was created.
        updated_at: When the client record was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: str
    phone: str | None
    birth_date: datetime | None
    allergies: str
    medical_conditions: str
    source: str | None
    image_rights: list[str]
    notes: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
