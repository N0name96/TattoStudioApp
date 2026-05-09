"""Consent status enumeration for the TattoStudioApp.

Defines all possible states of a consent document and valid transitions.
Used to track the lifecycle of a consent from creation to expiry or revocation.

Valid transitions:
    PENDING -> SIGNED (client signs the document)
    PENDING -> EXPIRED (consent expires before signing)
    SIGNED -> REVOKED (client revokes their consent)
"""

from enum import Enum


class ConsentStatus(str, Enum):
    """Represents the possible states of a consent document.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        PENDING: Consent created but not yet signed by the client.
        SIGNED: Consent has been signed by the client.
        EXPIRED: Consent validity period elapsed without signature.
        REVOKED: Consent was revoked by the client or admin.
    """

    PENDING = "pending"
    SIGNED = "signed"
    EXPIRED = "expired"
    REVOKED = "revoked"
