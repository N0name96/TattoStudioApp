"""Request DTOs for the clients module.

Contains Pydantic models for validating incoming client data.
These DTOs are used by the API layer and commands to validate input.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from domain.enums.client_source import ClientSource


class CreateClientRequest(BaseModel):
    """Request DTO for creating a new client.

    Contains all the data needed to register a client
    in the system.

    Attributes:
        full_name: Client's full name.
        email: Contact email address.
        phone: Optional phone number.
        birth_date: Optional birth date.
        allergies: Known allergies (default empty).
        medical_conditions: Known medical conditions (default empty).
        source: How the client discovered the studio.
        notes: Internal notes from the artist or admin.
    """

    full_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    birth_date: datetime | None = None
    allergies: str = Field(default="", max_length=1000)
    medical_conditions: str = Field(default="", max_length=1000)
    source: ClientSource | None = None
    notes: str = Field(default="", max_length=2000)
