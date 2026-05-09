"""Request DTOs for the artists module.

Contains Pydantic models for validating incoming artist data.
These DTOs are used by the API layer and commands to validate input.
"""

from pydantic import BaseModel, Field


class CreateArtistRequest(BaseModel):
    """Request DTO for creating a new artist.

    Contains all the data needed to register an artist
    in the system.

    Attributes:
        name: Artist full name.
        specialty: Artist specialty or style.
        email: Contact email for the artist.
        phone: Optional phone number.
        bio: Artist biography or profile description.
    """

    name: str = Field(min_length=1, max_length=100)
    specialty: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    bio: str | None = Field(default=None, max_length=1000)
