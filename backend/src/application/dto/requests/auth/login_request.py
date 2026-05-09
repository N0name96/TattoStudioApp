"""Request DTOs for the auth module.

Contains Pydantic models for validating incoming authentication data.
These DTOs are used by the API layer and commands to validate input.
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Request DTO for user login.

    Contains the credentials needed to authenticate a user.

    Attributes:
        email: User's email address.
        password: User's password.
    """

    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=1, max_length=128)
