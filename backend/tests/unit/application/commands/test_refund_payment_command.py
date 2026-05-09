"""Tests for the RefundPaymentCommand."""

from decimal import Decimal
from uuid import uuid4

import pytest

from application.commands.payments.refund_payment_command import (
    RefundPaymentCommand,
)
from core.errors import BusinessRuleError, EntityNotFoundError
from domain.entities.payment_entity import Payment
from infrastructure.persistence.in_memory.payment_repository import (
    InMemoryPaymentRepository,
)


class TestRefundPaymentCommand:
    """Tests for RefundPaymentCommand."""

    @pytest.fixture
    def payment_repo(self):
        return InMemoryPaymentRepository()

    @pytest.fixture
    def command(self, payment_repo):
        return RefundPaymentCommand(payment_repo)

    @pytest.mark.asyncio
    async def test_refund_completed_payment_success(self, command, payment_repo):
        """Test refunding a completed payment."""
        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )
        payment.complete(stripe_payment_id="pi_123456")
        await payment_repo.save(payment)

        response = await command.execute(payment.id)

        assert response.status == "refunded"

    @pytest.mark.asyncio
    async def test_refund_nonexistent_payment_raises_error(self, command):
        """Test refunding a non-existent payment raises EntityNotFoundError."""
        with pytest.raises(EntityNotFoundError, match="not found"):
            await command.execute(uuid4())

    @pytest.mark.asyncio
    async def test_refund_pending_payment_raises_error(self, command, payment_repo):
        """Test refunding a pending payment raises BusinessRuleError."""
        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )
        await payment_repo.save(payment)

        with pytest.raises(BusinessRuleError):
            await command.execute(payment.id)

    @pytest.mark.asyncio
    async def test_refund_already_refunded_payment_raises_error(
        self, command, payment_repo
    ):
        """Test refunding an already refunded payment raises BusinessRuleError."""
        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("100.00"),
        )
        payment.complete(stripe_payment_id="pi_123456")
        payment.refund()
        await payment_repo.save(payment)

        with pytest.raises(BusinessRuleError):
            await command.execute(payment.id)
