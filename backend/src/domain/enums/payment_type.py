"""Payment type enumeration for the TattoStudioApp.

Defines the different types of payments that can be recorded
for an appointment in the studio.

Used to distinguish between deposits, full payments, and
remaining balance payments.
"""

from enum import Enum


class PaymentType(str, Enum):
    """Represents the type of payment being made.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        DEPOSIT: A partial payment to reserve the appointment.
        FULL: Complete payment for the service.
        REMAINING: Payment of the remaining balance (total - deposit).
    """

    DEPOSIT = "deposit"
    FULL = "full"
    REMAINING = "remaining"
