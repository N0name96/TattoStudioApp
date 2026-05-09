"""Payment status enumeration for the TattoStudioApp.

Defines all possible states of a payment and valid transitions.
Used to track the lifecycle of a payment from creation to completion.

Valid transitions:
    PENDING -> COMPLETED (payment confirmed)
    PENDING -> FAILED (payment rejected)
    COMPLETED -> REFUNDED (refund processed)
"""

from enum import Enum


class PaymentStatus(str, Enum):
    """Represents the possible states of a payment.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        PENDING: Payment has been created but not yet processed.
        COMPLETED: Payment was successfully processed.
        FAILED: Payment processing failed.
        REFUNDED: Payment was refunded to the client.
    """

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
