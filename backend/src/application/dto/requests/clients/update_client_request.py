"""Request DTOs for updating clients.

Contains Pydantic models for validating incoming update data.
All fields are optional to support partial updates.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from domain.enums.client_source import ClientSource


class UpdateClientRequest(BaseModel):
    """Request DTO for updating client details.

    All fields are optional. Only provided fields will be updated.

    Attributes:
        full_name: New full name.
        email: New contact email.
        phone: New phone number.
        birth_date: New birth date.
        allergies: Updated allergies info.
        medical_conditions: Updated medical conditions info.
        source: Updated source channel.
        notes: Updated internal notes.
    """

    full_name: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    birth_date: datetime | None = None
    allergies: str | None = Field(default=None, max_length=1000)
    medical_conditions: str | None = Field(default=None, max_length=1000)
    source: ClientSource | None = None
    notes: str | None = Field(default=None, max_length=2000)
