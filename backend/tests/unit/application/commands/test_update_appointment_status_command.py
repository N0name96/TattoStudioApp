"""Tests for the UpdateAppointmentStatusCommand.

This module tests the appointment status update flow with mocked repositories
to isolate the command logic from infrastructure dependencies.
"""

from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.commands.appointments.update_appointment_status_command import (
    UpdateAppointmentStatusCommand,
)
from core.errors import BusinessRuleError, EntityNotFoundError
from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


@pytest.fixture
def mock_repo():
    """Create a mock appointment repository."""

    repo = AsyncMock()
    return repo


@pytest.fixture
def pending_appointment():
    """Create a pending appointment for testing."""

    now = datetime.now()

    return Appointment(
        id=uuid4(),
        client_id=uuid4(),
        artist_id=uuid4(),
        service_type=ServiceType.TATTOO,
        date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status=AppointmentStatus.PENDING,
        notes="Test appointment",
        total_price=100.0,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def confirmed_appointment():
    """Create a confirmed appointment for testing."""

    now = datetime.now()

    return Appointment(
        id=uuid4(),
        client_id=uuid4(),
        artist_id=uuid4(),
        service_type=ServiceType.TATTOO,
        date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status=AppointmentStatus.CONFIRMED,
        notes="Test appointment",
        total_price=100.0,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def in_progress_appointment():
    """Create an in-progress appointment for testing."""

    now = datetime.now()

    return Appointment(
        id=uuid4(),
        client_id=uuid4(),
        artist_id=uuid4(),
        service_type=ServiceType.TATTOO,
        date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status=AppointmentStatus.IN_PROGRESS,
        notes="Test appointment",
        total_price=100.0,
        created_at=now,
        updated_at=now,
    )


class TestUpdateAppointmentStatusCommand:
    """Tests for UpdateAppointmentStatusCommand.execute()."""

    @pytest.mark.asyncio
    async def test_accept_pending_appointment(self, mock_repo, pending_appointment):
        """Test accepting a pending appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act
        response = await command.execute(pending_appointment.id, "accept")

        # Assert
        assert response.status == AppointmentStatus.CONFIRMED
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_reject_pending_appointment(self, mock_repo, pending_appointment):
        """Test rejecting a pending appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act
        response = await command.execute(pending_appointment.id, "reject")

        # Assert
        assert response.status == AppointmentStatus.CANCELLED
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_confirmed_appointment(self, mock_repo, confirmed_appointment):
        """Test starting a confirmed appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = confirmed_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act
        response = await command.execute(confirmed_appointment.id, "start")

        # Assert
        assert response.status == AppointmentStatus.IN_PROGRESS
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_in_progress_appointment(self, mock_repo, in_progress_appointment):
        """Test completing an in-progress appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = in_progress_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act
        response = await command.execute(in_progress_appointment.id, "complete")

        # Assert
        assert response.status == AppointmentStatus.COMPLETED
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_pending_appointment(self, mock_repo, pending_appointment):
        """Test cancelling a pending appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act
        response = await command.execute(pending_appointment.id, "cancel")

        # Assert
        assert response.status == AppointmentStatus.CANCELLED
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_mark_no_show_in_progress_appointment(self, mock_repo, in_progress_appointment):
        """Test marking an in-progress appointment as no-show."""

        # Arrange
        mock_repo.get_by_id.return_value = in_progress_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act
        response = await command.execute(in_progress_appointment.id, "no_show")

        # Assert
        assert response.status == AppointmentStatus.NO_SHOW
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_entity_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised when appointment not found."""

        # Arrange
        mock_repo.get_by_id.return_value = None

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act & Assert
        with pytest.raises(EntityNotFoundError):
            await command.execute(uuid4(), "accept")

    @pytest.mark.asyncio
    async def test_raises_value_error_for_invalid_action(self, mock_repo, pending_appointment):
        """Test that ValueError is raised for invalid action."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act & Assert
        with pytest.raises(ValueError):
            await command.execute(pending_appointment.id, "invalid_action")

    @pytest.mark.asyncio
    async def test_raises_business_rule_error_for_invalid_transition(self, mock_repo, pending_appointment):
        """Test that BusinessRuleError is raised for invalid transition."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        command = UpdateAppointmentStatusCommand(mock_repo)

        # Act & Assert - Cannot start a pending appointment
        with pytest.raises(BusinessRuleError):
            await command.execute(pending_appointment.id, "start")
