"""Payment domain entity for the TattoStudioApp.

This module contains the Payment entity with all business logic
for payment lifecycle management including state transitions
and validation rules.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.payment_status import PaymentStatus
from domain.enums.payment_type import PaymentType


# Valid state transitions for payments
VALID_TRANSITIONS: dict[PaymentStatus, list[PaymentStatus]] = {
    PaymentStatus.PENDING: [
        PaymentStatus.COMPLETED,
        PaymentStatus.FAILED,
    ],
    PaymentStatus.COMPLETED: [
        PaymentStatus.REFUNDED,
    ],
    PaymentStatus.FAILED: [],
    PaymentStatus.REFUNDED: [],
}


@dataclass
class Payment:
    """Represents a payment for an appointment.

    This entity contains the core business logic for payment
    lifecycle management including state transitions.

    Attributes:
        id: Unique identifier for the payment.
        appointment_id: UUID of the associated appointment.
        amount: The payment amount as a Decimal.
        payment_type: Type of payment (deposit, full, remaining).
        status: Current status of the payment.
        stripe_payment_id: Payment ID from Stripe (if processed).
        created_at: When the payment was created.
        updated_at: When the payment was last updated.
    """

    id: UUID
    appointment_id: UUID
    amount: Decimal
    payment_type: PaymentType
    status: PaymentStatus
    stripe_payment_id: str | None
    created_at: datetime
    updated_at: datetime


    @classmethod
    def create(
        cls,
        appointment_id: UUID,
        amount: Decimal,
        payment_type: PaymentType = PaymentType.FULL,
    ) -> "Payment":
        """Create a new Payment entity with PENDING status.

        This is the factory method for creating payments.

        Args:
            appointment_id: UUID of the associated appointment.
            amount: The payment amount.
            payment_type: Type of payment (default FULL).

        Returns:
            A new Payment instance with PENDING status.

        Raises:
            BusinessRuleError: If the amount is zero or negative.
        """

        if amount <= 0:
            raise BusinessRuleError("Payment amount must be greater than zero")

        now = datetime.now()

        return cls(
            id=uuid4(),
            appointment_id=appointment_id,
            amount=amount,
            payment_type=payment_type,
            status=PaymentStatus.PENDING,
            stripe_payment_id=None,
            created_at=now,
            updated_at=now,
        )


    def _validate_transition(self, target_status: PaymentStatus) -> None:
        """Validate that a state transition is allowed.

        Args:
            target_status: The desired new status.

        Raises:
            BusinessRuleError: If the transition is not allowed.
        """

        allowed = VALID_TRANSITIONS.get(self.status, [])

        if target_status not in allowed:
            raise BusinessRuleError(
                f"Cannot transition payment from {self.status.value} to {target_status.value}"
            )


    def _update_status(self, target_status: PaymentStatus) -> None:
        """Update the status and timestamp after validation.

        Args:
            target_status: The new status to set.

        Raises:
            BusinessRuleError: If the transition is not allowed.
        """

        self._validate_transition(target_status)
        self.status = target_status
        self.updated_at = datetime.now()


    def complete(self, stripe_payment_id: str) -> None:
        """Mark the payment as completed after successful Stripe processing.

        Args:
            stripe_payment_id: The Stripe payment intent ID.

        Raises:
            BusinessRuleError: If the payment is not in PENDING status.
        """

        self._update_status(PaymentStatus.COMPLETED)
        self.stripe_payment_id = stripe_payment_id


    def fail(self) -> None:
        """Mark the payment as failed.

        Called when Stripe payment processing fails.

        Raises:
            BusinessRuleError: If the payment is not in PENDING status.
        """

        self._update_status(PaymentStatus.FAILED)


    def refund(self) -> None:
        """Mark the payment as refunded.

        Called after a successful Stripe refund.

        Raises:
            BusinessRuleError: If the payment is not in COMPLETED status.
        """

        self._update_status(PaymentStatus.REFUNDED)
