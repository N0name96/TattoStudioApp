"""Response DTO for consent data."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.enums.consent_status import ConsentStatus
from domain.enums.consent_type import ConsentType


class ConsentResponse(BaseModel):
    """Response DTO for consent data.

    Used to return consent information to the API client.
    Maps from domain entity to a serializable format.

    Note: The token is included so it can be embedded in a QR code
    or sent as a link to the client. It is NOT included in list
    responses for security (filter at query level).

    Attributes:
        id: Unique identifier for the consent.
        client_id: UUID of the client who must sign.
        appointment_id: Optional UUID of the associated appointment.
        consent_type: Type of consent document.
        status: Current status of the consent.
        token: Unique token for accessing the consent remotely.
        signature_data: Base64-encoded signature data (only when signed).
        signed_at: When the consent was signed.
        expires_at: When the consent expires if not signed.
        created_at: When the consent was created.
        updated_at: When the consent was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_id: UUID
    appointment_id: UUID | None
    consent_type: ConsentType
    status: ConsentStatus
    token: str
    signature_data: str | None
    signed_at: datetime | None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
