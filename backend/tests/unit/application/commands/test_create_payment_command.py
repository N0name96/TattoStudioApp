"""Tests for the CreatePaymentCommand."""

from datetime import date, time
from decimal import Decimal
from uuid import uuid4

import pytest

from application.commands.payments.create_payment_command import (
    CreatePaymentCommand,
)
from application.dto.requests.payments.create_payment_request import (
    CreatePaymentRequest,
)
from core.errors import EntityNotFoundError
from domain.entities.appointment_entity import Appointment
from domain.enums.payment_status import PaymentStatus
from domain.enums.payment_type import PaymentType
from domain.enums.service_type import ServiceType
from infrastructure.persistence.in_memory.appointment_repository import (
    InMemoryAppointmentRepository,
)
from infrastructure.persistence.in_memory.payment_repository import (
    InMemoryPaymentRepository,
)


class TestCreatePaymentCommand:
    """Tests for CreatePaymentCommand."""

    @pytest.fixture
    def payment_repo(self):
        return InMemoryPaymentRepository()

    @pytest.fixture
    def appointment_repo(self):
        return InMemoryAppointmentRepository()

    @pytest.fixture
    def command(self, payment_repo, appointment_repo):
        return CreatePaymentCommand(payment_repo, appointment_repo)

    @pytest.mark.asyncio
    async def test_create_payment_success(self, command, appointment_repo):
        """Test creating a payment for an existing appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date(2026, 5, 10),
            start_time=time(10, 0),
            total_price=150.0,
        )
        await appointment_repo.save(appointment)

        request = CreatePaymentRequest(
            appointment_id=appointment.id,
            amount=Decimal("100.00"),
            payment_type=PaymentType.DEPOSIT,
        )

        response = await command.execute(request)

        assert response.id is not None
        assert response.appointment_id == appointment.id
        assert response.amount == Decimal("100.00")
        assert response.payment_type == PaymentType.DEPOSIT
        assert response.status == PaymentStatus.PENDING
        assert response.stripe_payment_id is None

    @pytest.mark.asyncio
    async def test_create_payment_appointment_not_found_raises_error(
        self, command
    ):
        """Test that creating a payment for a non-existent appointment fails."""

        request = CreatePaymentRequest(
            appointment_id=uuid4(),
            amount=Decimal("50.00"),
        )

        with pytest.raises(EntityNotFoundError, match="not found"):
            await command.execute(request)

    @pytest.mark.asyncio
    async def test_created_payment_is_persisted(
        self, command, payment_repo, appointment_repo
    ):
        """Test that the created payment is actually persisted."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date(2026, 6, 1),
            start_time=time(10, 0),
        )
        await appointment_repo.save(appointment)

        request = CreatePaymentRequest(
            appointment_id=appointment.id,
            amount=Decimal("200.00"),
        )

        response = await command.execute(request)

        persisted = await payment_repo.get_by_id(response.id)
        assert persisted is not None
        assert persisted.amount == Decimal("200.00")
