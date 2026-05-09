"""Tests for the UpdateAppointmentDetailsCommand.

This module tests the appointment details update flow with mocked repositories
to isolate the command logic from infrastructure dependencies.
"""

from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.commands.appointments.update_appointment_details_command import (
    UpdateAppointmentDetailsCommand,
)
from application.dto.requests.appointments.update_appointment_details_request import (
    UpdateAppointmentDetailsRequest,
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


class TestUpdateAppointmentDetailsCommand:
    """Tests for UpdateAppointmentDetailsCommand.execute()."""

    @pytest.mark.asyncio
    async def test_update_details_success(self, mock_repo, pending_appointment):
        """Test successful appointment details update."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        request = UpdateAppointmentDetailsRequest(
            notes="Updated notes",
            total_price=150.0,
        )

        command = UpdateAppointmentDetailsCommand(mock_repo)

        # Act
        response = await command.execute(pending_appointment.id, request)

        # Assert
        assert response.notes == "Updated notes"
        assert response.total_price == 150.0
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_details_partial_update(self, mock_repo, pending_appointment):
        """Test partial update only changes provided fields."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        request = UpdateAppointmentDetailsRequest(notes="Only notes changed")

        command = UpdateAppointmentDetailsCommand(mock_repo)

        # Act
        response = await command.execute(pending_appointment.id, request)

        # Assert
        assert response.notes == "Only notes changed"
        assert response.total_price == 100.0  # Unchanged
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_details_date_and_time(self, mock_repo, pending_appointment):
        """Test updating date and start time recalculates end time."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        new_date = date.today() + timedelta(days=14)
        new_time = time(14, 0)

        request = UpdateAppointmentDetailsRequest(
            date=new_date,
            start_time=new_time,
        )

        command = UpdateAppointmentDetailsCommand(mock_repo)

        # Act
        response = await command.execute(pending_appointment.id, request)

        # Assert
        assert response.date == new_date
        assert response.start_time == new_time
        # Tattoo is 120 min, so 14:00 + 120 min = 16:00
        assert response.end_time == time(16, 0)
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_details_raises_entity_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised when appointment not found."""

        # Arrange
        mock_repo.get_by_id.return_value = None

        request = UpdateAppointmentDetailsRequest(notes="Updated")

        command = UpdateAppointmentDetailsCommand(mock_repo)

        # Act & Assert
        with pytest.raises(EntityNotFoundError):
            await command.execute(uuid4(), request)

    @pytest.mark.asyncio
    async def test_update_details_raises_for_completed_status(self, mock_repo, completed_appointment):
        """Test that BusinessRuleError is raised for non-mutable status."""

        # Arrange
        mock_repo.get_by_id.return_value = completed_appointment

        request = UpdateAppointmentDetailsRequest(notes="Should fail")

        command = UpdateAppointmentDetailsCommand(mock_repo)

        # Act & Assert
        with pytest.raises(BusinessRuleError):
            await command.execute(completed_appointment.id, request)

    @pytest.mark.asyncio
    async def test_update_details_persists_changes(self, mock_repo, pending_appointment):
        """Test that changes are persisted to the repository."""

        # Arrange
        mock_repo.get_by_id.return_value = pending_appointment
        mock_repo.save.side_effect = lambda a: a

        request = UpdateAppointmentDetailsRequest(total_price=200.0)

        command = UpdateAppointmentDetailsCommand(mock_repo)

        # Act
        await command.execute(pending_appointment.id, request)

        # Assert
        mock_repo.save.assert_called_once()
        saved_appointment = mock_repo.save.call_args[0][0]
        assert saved_appointment.total_price == 200.0
