"""Consent domain entity for the TattoStudioApp.

This module contains the Consent entity with all business logic
for consent lifecycle management including state transitions,
signature validation, and expiry checks.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.consent_status import ConsentStatus
from domain.enums.consent_type import ConsentType


# Default validity period for a consent before it expires (72 hours)
DEFAULT_CONSENT_VALIDITY_HOURS = 72

# Valid state transitions
VALID_TRANSITIONS: dict[ConsentStatus, list[ConsentStatus]] = {
    ConsentStatus.PENDING: [
        ConsentStatus.SIGNED,
        ConsentStatus.EXPIRED,
    ],
    ConsentStatus.SIGNED: [
        ConsentStatus.REVOKED,
    ],
    ConsentStatus.EXPIRED: [],
    ConsentStatus.REVOKED: [],
}


def _generate_token() -> str:
    """Generate a unique URL-safe token for consent access."""

    return secrets.token_urlsafe(32)


@dataclass
class Consent:
    """Represents a legal consent document for a client.

    This entity manages the consent lifecycle: creation with a unique token,
    signing by the client, expiry if not signed in time, and revocation.

    Each consent is linked to a client and optionally to an appointment.
    A unique token allows access via QR code or remote link.

    Attributes:
        id: Unique identifier for the consent.
        client_id: UUID of the client who must sign the consent.
        appointment_id: Optional UUID of the associated appointment.
        consent_type: Type of consent document.
        status: Current status of the consent.
        token: Unique URL-safe token for accessing the consent remotely.
        signature_data: Base64-encoded signature data (set when signed).
        signed_at: Timestamp of when the consent was signed.
        expires_at: Timestamp after which the consent is no longer valid.
        created_at: When the consent was created.
        updated_at: When the consent was last updated.
    """

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


    @classmethod
    def create(
        cls,
        client_id: UUID,
        consent_type: ConsentType,
        appointment_id: UUID | None = None,
        validity_hours: int = DEFAULT_CONSENT_VALIDITY_HOURS,
    ) -> "Consent":
        """Create a new Consent entity with PENDING status.

        Generates a unique token for access via QR or remote link.
        The consent expires after `validity_hours` if not signed.

        Args:
            client_id: UUID of the client who must sign.
            consent_type: Type of consent being requested.
            appointment_id: Optional UUID of the associated appointment.
            validity_hours: Hours until the consent expires (default 72).

        Returns:
            A new Consent instance with PENDING status.

        Raises:
            BusinessRuleError: If validity_hours is not positive.
        """

        if validity_hours <= 0:
            raise BusinessRuleError("Validity period must be greater than zero")

        now = datetime.now()

        return cls(
            id=uuid4(),
            client_id=client_id,
            appointment_id=appointment_id,
            consent_type=consent_type,
            status=ConsentStatus.PENDING,
            token=_generate_token(),
            signature_data=None,
            signed_at=None,
            expires_at=now + timedelta(hours=validity_hours),
            created_at=now,
            updated_at=now,
        )


    def _validate_transition(self, target_status: ConsentStatus) -> None:
        """Validate that a state transition is allowed.

        Args:
            target_status: The desired new status.

        Raises:
            BusinessRuleError: If the transition is not allowed.
        """

        allowed = VALID_TRANSITIONS.get(self.status, [])

        if target_status not in allowed:
            raise BusinessRuleError(
                f"Cannot transition consent from {self.status.value} to {target_status.value}"
            )


    def _update_status(self, target_status: ConsentStatus) -> None:
        """Update the status and timestamp after validation.

        Args:
            target_status: The new status to set.

        Raises:
            BusinessRuleError: If the transition is not allowed.
        """

        self._validate_transition(target_status)
        self.status = target_status
        self.updated_at = datetime.now()


    def sign(self, signature_data: str) -> None:
        """Sign the consent with the client's signature.

        Only valid for PENDING consents that have not expired.

        Args:
            signature_data: Base64-encoded representation of the signature.

        Raises:
            BusinessRuleError: If the consent is not in PENDING status.
            BusinessRuleError: If the consent has already expired.
        """

        if self._is_expired():
            raise BusinessRuleError("Cannot sign an expired consent")

        self._update_status(ConsentStatus.SIGNED)
        self.signature_data = signature_data
        self.signed_at = datetime.now()


    def expire(self) -> None:
        """Mark the consent as expired.

        Called when the consent validity period has elapsed without
        a signature from the client. Only valid for PENDING consents.

        Raises:
            BusinessRuleError: If the consent is not in PENDING status.
        """

        self._update_status(ConsentStatus.EXPIRED)


    def revoke(self) -> None:
        """Revoke a previously signed consent.

        The client or admin can revoke a signed consent at any time.
        Once revoked, the consent is no longer legally valid.

        Raises:
            BusinessRuleError: If the consent is not in SIGNED status.
        """

        self._update_status(ConsentStatus.REVOKED)


    def _is_expired(self) -> bool:
        """Check if the consent has expired based on the expires_at timestamp.

        Returns:
            True if the current time is past the expires_at timestamp.
        """

        return datetime.now() > self.expires_at


    def renew(self, additional_hours: int = DEFAULT_CONSENT_VALIDITY_HOURS) -> None:
        """Renew the consent expiration time.

        Only valid for PENDING consents. Extends expires_at from now.

        Args:
            additional_hours: Number of hours to extend (default 72).

        Raises:
            BusinessRuleError: If the consent is not in PENDING status.
            BusinessRuleError: If additional_hours is not positive.
        """

        if self.status != ConsentStatus.PENDING:
            raise BusinessRuleError(
                f"Cannot renew consent in {self.status.value} status"
            )

        if additional_hours <= 0:
            raise BusinessRuleError("Renewal hours must be greater than zero")

        self.expires_at = datetime.now() + timedelta(hours=additional_hours)
        self.updated_at = datetime.now()
