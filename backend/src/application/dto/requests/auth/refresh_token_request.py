"""Request DTOs for the auth module.

Contains Pydantic models for validating incoming authentication data.
These DTOs are used by the API layer and commands to validate input.
"""

from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    """Request DTO for token refresh.

    Contains the refresh token needed to obtain a new access token.

    Attributes:
        refresh_token: The JWT refresh token.
    """

    refresh_token: str = Field(..., min_length=1)
