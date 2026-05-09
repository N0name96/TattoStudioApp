"""Request DTOs for updating artists.

Contains Pydantic models for validating incoming update data.
All fields are optional to support partial updates.
"""

from pydantic import BaseModel, Field


class UpdateArtistRequest(BaseModel):
    """Request DTO for updating artist details.

    All fields are optional. Only provided fields will be updated.

    Attributes:
        name: New artist name.
        specialty: New specialty.
        email: New contact email.
        phone: New phone number.
        bio: New biography.
        is_active: New active status.
    """

    name: str | None = Field(default=None, max_length=100)
    specialty: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    bio: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None
