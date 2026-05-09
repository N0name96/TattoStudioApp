"""Request DTO for signing a consent."""

from pydantic import BaseModel, Field


class SignConsentRequest(BaseModel):
    """Request DTO for signing a consent document.

    Contains the signature data submitted by the client.

    Attributes:
        signature_data: Base64-encoded representation of the client's signature.
    """

    signature_data: str = Field(min_length=1)
