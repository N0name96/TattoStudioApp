"""Tests for the DeleteAppointmentCommand.

This module tests the appointment deletion flow with mocked repositories
to isolate the command logic from infrastructure dependencies.
"""

from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.commands.appointments.delete_appointment_command import (
    DeleteAppointmentCommand,
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
def cancelled_appointment():
    """Create a cancelled appointment for testing."""

    now = datetime.now()

    return Appointment(
        id=uuid4(),
        client_id=uuid4(),
        artist_id=uuid4(),
        service_type=ServiceType.TATTOO,
        date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status=AppointmentStatus.CANCELLED,
        notes="Test appointment",
        total_price=100.0,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def completed_appointment():
    """Create a completed appointment for testing."""

    now = datetime.now()

    return Appointment(
        id=uuid4(),
        client_id=uuid4(),
        artist_id=uuid4(),
        service_type=ServiceType.TATTOO,
        date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status=AppointmentStatus.COMPLETED,
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


class TestDeleteAppointmentCommand:
    """Tests for DeleteAppointmentCommand.execute()."""

    @pytest.mark.asyncio
    async def test_delete_pending_appointment(self, mock_repo, pending_appointment):
        """Test successful deletion of a pending appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment

        command = DeleteAppointmentCommand(mock_repo)

        # Act
        await command.execute(pending_appointment.id)

        # Assert
        mock_repo.delete.assert_called_once_with(pending_appointment.id)

    @pytest.mark.asyncio
    async def test_delete_cancelled_appointment(self, mock_repo, cancelled_appointment):
        """Test successful deletion of a cancelled appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = cancelled_appointment

        command = DeleteAppointmentCommand(mock_repo)

        # Act
        await command.execute(cancelled_appointment.id)

        # Assert
        mock_repo.delete.assert_called_once_with(cancelled_appointment.id)

    @pytest.mark.asyncio
    async def test_delete_raises_entity_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised when appointment not found."""

        # Arrange
        mock_repo.get_by_id.return_value = None

        command = DeleteAppointmentCommand(mock_repo)

        # Act & Assert
        with pytest.raises(EntityNotFoundError):
            await command.execute(uuid4())

    @pytest.mark.asyncio
    async def test_delete_raises_for_completed_appointment(self, mock_repo, completed_appointment):
        """Test that BusinessRuleError is raised for completed appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = completed_appointment

        command = DeleteAppointmentCommand(mock_repo)

        # Act & Assert
        with pytest.raises(BusinessRuleError):
            await command.execute(completed_appointment.id)

    @pytest.mark.asyncio
    async def test_delete_raises_for_in_progress_appointment(self, mock_repo, in_progress_appointment):
        """Test that BusinessRuleError is raised for in-progress appointment."""

        # Arrange
        mock_repo.get_by_id.return_value = in_progress_appointment

        command = DeleteAppointmentCommand(mock_repo)

        # Act & Assert
        with pytest.raises(BusinessRuleError):
            await command.execute(in_progress_appointment.id)
