"""Request DTOs for the auth module.

Contains Pydantic models for validating incoming authentication data.
These DTOs are used by the API layer and commands to validate input.
"""

from pydantic import BaseModel, Field

from domain.enums.user_role import UserRole


class RegisterRequest(BaseModel):
    """Request DTO for user registration.

    Contains all the data needed to create a new user account.

    Attributes:
        email: User's email address (must be valid format).
        password: User's password (minimum 8 characters).
        full_name: User's full name.
        role: User's role (default: client).
        phone: Optional phone number.
    """

    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.CLIENT
    phone: str | None = Field(default=None, max_length=20)
