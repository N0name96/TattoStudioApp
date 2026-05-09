"""Tests for the CreateAppointmentCommand.

This module tests the appointment creation flow with mocked repositories
to isolate the command logic from infrastructure dependencies.
"""


from datetime import date, time, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from application.commands.appointments.create_appointment_command import (
    CreateAppointmentCommand,
)
from application.dto.requests.appointments.create_appointment_request import (
    CreateAppointmentRequest,
)
from core.errors import BusinessRuleError
from domain.entities.appointment_entity import Appointment
from domain.enums.service_type import ServiceType


@pytest.fixture
def mock_repo():
    """Create a mock appointment repository."""

    repo = AsyncMock()
    return repo


@pytest.fixture
def valid_request():
    """Create a valid appointment creation request."""

    return CreateAppointmentRequest(
        artist_id=uuid4(),
        service_type=ServiceType.TATTOO,
        date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        notes="First session",
    )


class TestCreateAppointmentCommand:
    """Tests for CreateAppointmentCommand.execute()."""

    @pytest.mark.asyncio
    async def test_create_appointment_success(self, mock_repo, valid_request):
        """Test successful appointment creation."""

        # Arrange
        client_id = uuid4()
        mock_repo.find_by_artist_and_date.return_value = None
        mock_repo.save.side_effect = lambda a: a

        command = CreateAppointmentCommand(mock_repo)

        # Act
        response = await command.execute(client_id, valid_request)

        # Assert
        assert response.client_id == client_id
        assert response.artist_id == valid_request.artist_id
        assert response.service_type == ServiceType.TATTOO
        assert response.status.value == "pending"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_appointment_checks_availability(self, mock_repo, valid_request):
        """Test that availability is checked before creating."""

        # Arrange
        client_id = uuid4()
        mock_repo.find_by_artist_and_date.return_value = None
        mock_repo.save.side_effect = lambda a: a

        command = CreateAppointmentCommand(mock_repo)

        # Act
        await command.execute(client_id, valid_request)

        # Assert
        mock_repo.find_by_artist_and_date.assert_called_once_with(
            artist_id=valid_request.artist_id,
            appointment_date=valid_request.date,
            start_time=valid_request.start_time,
        )

    @pytest.mark.asyncio
    async def test_create_appointment_raises_if_not_available(self, mock_repo, valid_request):
        """Test that BusinessRuleError is raised when artist is not available."""

        # Arrange
        client_id = uuid4()
        existing_appointment = MagicMock()
        mock_repo.find_by_artist_and_date.return_value = existing_appointment

        command = CreateAppointmentCommand(mock_repo)

        # Act & Assert
        with pytest.raises(BusinessRuleError):
            await command.execute(client_id, valid_request)

    @pytest.mark.asyncio
    async def test_create_appointment_persists(self, mock_repo, valid_request):
        """Test that the appointment is saved to the repository."""

        # Arrange
        client_id = uuid4()
        mock_repo.find_by_artist_and_date.return_value = None
        mock_repo.save.side_effect = lambda a: a

        command = CreateAppointmentCommand(mock_repo)

        # Act
        await command.execute(client_id, valid_request)

        # Assert
        mock_repo.save.assert_called_once()
        saved_appointment = mock_repo.save.call_args[0][0]
        assert isinstance(saved_appointment, Appointment)
        assert saved_appointment.client_id == client_id
