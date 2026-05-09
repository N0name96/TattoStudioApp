"""Response DTOs for the artists module.

Contains Pydantic models for serializing artist data.
These DTOs are used by the API layer to format responses.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ArtistResponse(BaseModel):
    """Response DTO for artist data.

    Used to return artist information to the API client.
    Maps from domain entity to a serializable format.

    Attributes:
        id: Unique identifier for the artist.
        name: Artist full name.
        specialty: Artist specialty or style.
        email: Contact email for the artist.
        phone: Optional phone number.
        bio: Artist biography or profile description.
        is_active: Whether the artist is currently active.
        created_at: When the artist was created.
        updated_at: When the artist was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    specialty: str
    email: str
    phone: str | None
    bio: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
