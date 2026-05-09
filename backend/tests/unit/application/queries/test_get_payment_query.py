"""Tests for the GetPaymentQuery."""

from decimal import Decimal
from uuid import uuid4

import pytest

from application.queries.payments.get_payment_query import GetPaymentQuery
from core.errors import EntityNotFoundError
from domain.entities.payment_entity import Payment
from infrastructure.persistence.in_memory.payment_repository import (
    InMemoryPaymentRepository,
)


class TestGetPaymentQuery:
    """Tests for GetPaymentQuery."""

    @pytest.fixture
    def payment_repo(self):
        return InMemoryPaymentRepository()

    @pytest.fixture
    def query(self, payment_repo):
        return GetPaymentQuery(payment_repo)

    @pytest.mark.asyncio
    async def test_get_existing_payment(self, query, payment_repo):
        """Test retrieving an existing payment."""
        payment = Payment.create(
            appointment_id=uuid4(),
            amount=Decimal("150.00"),
        )
        await payment_repo.save(payment)

        response = await query.execute(payment.id)

        assert response.id == payment.id
        assert response.amount == Decimal("150.00")

    @pytest.mark.asyncio
    async def test_get_nonexistent_payment_raises_error(self, query):
        """Test that retrieving a non-existent payment raises EntityNotFoundError."""
        with pytest.raises(EntityNotFoundError, match="not found"):
            await query.execute(uuid4())
