"""Request DTO for creating a consent."""

from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.consent_type import ConsentType


class CreateConsentRequest(BaseModel):
    """Request DTO for creating a new consent document.

    Contains the data needed to generate a consent for a client.

    Attributes:
        client_id: UUID of the client who must sign the consent.
        consent_type: Type of consent document.
        appointment_id: Optional UUID of the associated appointment.
    """

    client_id: UUID
    consent_type: ConsentType
    appointment_id: UUID | None = None
