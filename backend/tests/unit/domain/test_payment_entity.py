"""Tests for the Payment domain entity.

This module tests the pure business logic of the Payment entity,
including creation, state transitions, and validation rules.

No mocks are needed since the entity has no external dependencies.
"""

from decimal import Decimal
from uuid import uuid4

import pytest

from core.errors import BusinessRuleError
from domain.entities.payment_entity import Payment
from domain.enums.payment_status import PaymentStatus
from domain.enums.payment_type import PaymentType


class TestPaymentCreation:
    """Tests for Payment.create() factory method."""

    def test_create_payment_with_valid_data(self):
        """Test that a valid payment can be created."""

        appointment_id = uuid4()

        payment = Payment.create(
            appointment_id=appointment_id,
            amount=Decimal("100.00"),
            payment_type=PaymentType.FULL,
        )

        assert payment.appointment_id == appointment_id
        assert payment.amount == Decimal("100.00")
        assert payment.payment_type == PaymentType.FULL
        assert payment.status == PaymentStatus.PENDING
        assert payment.stripe_payment_id is None

    def test_create_payment_with_default_type(self):
        """Test that the default payment type is FULL."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("50.00"),
        )

        assert payment.payment_type == PaymentType.FULL

    def test_create_payment_with_negative_amount_raises_error(self):
        """Test that creating a payment with zero or negative amount fails."""

        with pytest.raises(BusinessRuleError, match="greater than zero"):
            Payment.create(
                appointment_id=uuid4(),
                amount=Decimal("-10.00"),
            )

    def test_create_payment_with_zero_amount_raises_error(self):
        """Test that creating a payment with zero amount fails."""

        with pytest.raises(BusinessRuleError, match="greater than zero"):
            Payment.create(
                appointment_id=uuid4(),
                amount=Decimal("0.00"),
            )

    def test_create_payment_with_deposit_type(self):
        """Test creating a deposit payment."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("30.00"),
            payment_type=PaymentType.DEPOSIT,
        )

        assert payment.payment_type == PaymentType.DEPOSIT

    def test_create_payment_has_unique_id(self):
        """Test that each payment gets a unique ID."""

        appointment_id = uuid4()

        payment1 = Payment.create(appointment_id=appointment_id, amount=Decimal("50.00"))
        payment2 = Payment.create(appointment_id=appointment_id, amount=Decimal("75.00"))

        assert payment1.id != payment2.id


class TestPaymentTransitions:
    """Tests for payment state transitions."""

    def test_complete_pending_payment(self):
        """Test completing a pending payment."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.complete(stripe_payment_id="pi_123456")

        assert payment.status == PaymentStatus.COMPLETED
        assert payment.stripe_payment_id == "pi_123456"

    def test_fail_pending_payment(self):
        """Test failing a pending payment."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.fail()

        assert payment.status == PaymentStatus.FAILED

    def test_refund_completed_payment(self):
        """Test refunding a completed payment."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.complete(stripe_payment_id="pi_123456")
        payment.refund()

        assert payment.status == PaymentStatus.REFUNDED


class TestInvalidTransitions:
    """Tests for invalid state transitions."""

    def test_cannot_complete_non_pending_payment(self):
        """Test that completing a non-pending payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.complete(stripe_payment_id="pi_123456")

        with pytest.raises(BusinessRuleError):
            payment.complete(stripe_payment_id="pi_789")

    def test_cannot_fail_completed_payment(self):
        """Test that failing a completed payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.complete(stripe_payment_id="pi_123456")

        with pytest.raises(BusinessRuleError):
            payment.fail()

    def test_cannot_fail_refunded_payment(self):
        """Test that failing a refunded payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.complete(stripe_payment_id="pi_123456")
        payment.refund()

        with pytest.raises(BusinessRuleError):
            payment.fail()

    def test_cannot_refund_pending_payment(self):
        """Test that refunding a pending payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        with pytest.raises(BusinessRuleError):
            payment.refund()

    def test_cannot_refund_failed_payment(self):
        """Test that refunding a failed payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.fail()

        with pytest.raises(BusinessRuleError):
            payment.refund()

    def test_cannot_refund_already_refunded_payment(self):
        """Test that refunding an already refunded payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.complete(stripe_payment_id="pi_123456")
        payment.refund()

        with pytest.raises(BusinessRuleError):
            payment.refund()

    def test_cannot_complete_failed_payment(self):
        """Test that completing a failed payment raises error."""

        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )

        payment.fail()

        with pytest.raises(BusinessRuleError):
            payment.complete(stripe_payment_id="pi_789")
