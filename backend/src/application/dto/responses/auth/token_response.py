"""Response DTOs for the auth module.

Contains Pydantic models for serializing authentication data.
These DTOs are used by the API layer to format responses.
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Response DTO for authentication tokens.

    Returned after successful login or token refresh.

    Attributes:
        access_token: JWT access token for API authentication.
        refresh_token: JWT refresh token for obtaining new access tokens.
        token_type: Type of token (always "bearer").
        expires_in: Access token validity in seconds.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
