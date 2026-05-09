"""Request DTO for payments module."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.payment_type import PaymentType


class CreatePaymentRequest(BaseModel):
    """Request DTO for creating a new payment.

    Contains all the data needed to initiate a payment
    for an appointment.

    Attributes:
        appointment_id: UUID of the appointment this payment is for.
        amount: The payment amount (must be greater than zero).
        payment_type: Type of payment being made.
    """

    appointment_id: UUID
    amount: Decimal = Field(gt=0)
    payment_type: PaymentType = PaymentType.FULL
