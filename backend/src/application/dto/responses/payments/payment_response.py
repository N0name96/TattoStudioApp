"""Response DTOs for the payments module."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.enums.payment_status import PaymentStatus
from domain.enums.payment_type import PaymentType


class PaymentResponse(BaseModel):
    """Response DTO for payment data.

    Used to return payment information to the API client.
    Maps from domain entity to a serializable format.

    Attributes:
        id: Unique identifier for the payment.
        appointment_id: UUID of the associated appointment.
        amount: The payment amount.
        payment_type: Type of payment (deposit, full, remaining).
        status: Current status of the payment.
        stripe_payment_id: Payment ID from Stripe (if processed).
        created_at: When the payment was created.
        updated_at: When the payment was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    appointment_id: UUID
    amount: Decimal
    payment_type: PaymentType
    status: PaymentStatus
    stripe_payment_id: str | None
    created_at: datetime
    updated_at: datetime
