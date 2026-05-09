"""Response DTOs for the auth module.

Contains Pydantic models for serializing authentication data.
These DTOs are used by the API layer to format responses.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.enums.user_role import UserRole


class UserResponse(BaseModel):
    """Response DTO for user data.

    Used to return user information to the API client.
    Maps from domain entity to a serializable format.

    Attributes:
        id: Unique identifier for the user.
        email: User's email address.
        full_name: User's full name.
        role: User's role in the system.
        phone: Optional phone number.
        is_active: Whether the user account is active.
        created_at: When the user was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: str
    role: UserRole
    phone: str | None
    is_active: bool
    created_at: datetime
