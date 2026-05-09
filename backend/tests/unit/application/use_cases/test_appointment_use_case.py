"""Tests for the AppointmentUseCase.

This module tests that the use case correctly delegates to commands and queries.
Uses mocked commands/queries to isolate the orchestration logic.
"""

from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.dto.requests.appointments.create_appointment_request import (
    CreateAppointmentRequest,
)
from application.dto.requests.appointments.update_appointment_details_request import (
    UpdateAppointmentDetailsRequest,
)
from application.use_cases.appointments.appointment_use_case import (
    AppointmentUseCase,
)
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


@pytest.fixture
def mock_repo():
    """Create a mock appointment repository."""

    repo = AsyncMock()
    return repo


@pytest.fixture
def use_case(mock_repo):
    """Create an AppointmentUseCase with mocked repository."""

    return AppointmentUseCase(appointment_repo=mock_repo)


class TestAppointmentUseCase:
    """Tests for AppointmentUseCase delegation."""

    @pytest.mark.asyncio
    async def test_create_appointment_delegates_to_command(self, use_case, mock_repo):
        """Test that create_appointment delegates to CreateAppointmentCommand."""

        # Arrange
        client_id = uuid4()
        request = CreateAppointmentRequest(
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=7),
            start_time=time(10, 0),
        )
        mock_repo.find_by_artist_and_date.return_value = None
        mock_repo.save.side_effect = lambda a: a

        # Act
        response = await use_case.create_appointment(client_id, request)

        # Assert
        assert response is not None
        assert response.client_id == client_id
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_appointment_delegates_to_query(self, use_case, mock_repo):
        """Test that get_appointment delegates to GetAppointmentQuery."""

        # Arrange
        appointment_id = uuid4()
        now = datetime.now()

        from domain.entities.appointment_entity import Appointment

        appointment = Appointment(
            id=appointment_id,
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=7),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status=AppointmentStatus.PENDING,
            notes=None,
            total_price=0.0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = appointment

        # Act
        response = await use_case.get_appointment(appointment_id)

        # Assert
        assert response.id == appointment_id
        mock_repo.get_by_id.assert_called_once_with(appointment_id)

    @pytest.mark.asyncio
    async def test_list_appointments_delegates_to_query(self, use_case, mock_repo):
        """Test that list_appointments delegates to ListAppointmentsQuery."""

        # Arrange
        mock_repo.list_all.return_value = []

        # Act
        result = await use_case.list_appointments()

        # Assert
        assert result == []
        mock_repo.list_all.assert_called_once_with(status=None)

    @pytest.mark.asyncio
    async def test_accept_appointment_delegates_to_status_command(self, use_case, mock_repo):
        """Test that accept_appointment delegates to UpdateAppointmentStatusCommand."""

        # Arrange
        appointment_id = uuid4()
        now = datetime.now()

        from domain.entities.appointment_entity import Appointment

        appointment = Appointment(
            id=appointment_id,
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=7),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status=AppointmentStatus.PENDING,
            notes=None,
            total_price=0.0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = appointment
        mock_repo.save.side_effect = lambda a: a

        # Act
        response = await use_case.accept_appointment(appointment_id)

        # Assert
        assert response.status == AppointmentStatus.CONFIRMED
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_appointment_details_delegates_to_command(self, use_case, mock_repo):
        """Test that update_appointment_details delegates to UpdateAppointmentDetailsCommand."""

        # Arrange
        appointment_id = uuid4()
        now = datetime.now()

        from domain.entities.appointment_entity import Appointment

        appointment = Appointment(
            id=appointment_id,
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=7),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status=AppointmentStatus.PENDING,
            notes="Original notes",
            total_price=100.0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = appointment
        mock_repo.save.side_effect = lambda a: a

        request = UpdateAppointmentDetailsRequest(notes="Updated notes")

        # Act
        response = await use_case.update_appointment_details(appointment_id, request)

        # Assert
        assert response.notes == "Updated notes"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_appointment_delegates_to_command(self, use_case, mock_repo):
        """Test that delete_appointment delegates to DeleteAppointmentCommand."""

        # Arrange
        appointment_id = uuid4()
        now = datetime.now()

        from domain.entities.appointment_entity import Appointment

        appointment = Appointment(
            id=appointment_id,
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=7),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status=AppointmentStatus.PENDING,
            notes=None,
            total_price=0.0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = appointment

        # Act
        await use_case.delete_appointment(appointment_id)

        # Assert
        mock_repo.delete.assert_called_once_with(appointment_id)

    @pytest.mark.asyncio
    async def test_mark_no_show_delegates_to_status_command(self, use_case, mock_repo):
        """Test that mark_no_show delegates to UpdateAppointmentStatusCommand."""

        # Arrange
        appointment_id = uuid4()
        now = datetime.now()

        from domain.entities.appointment_entity import Appointment

        appointment = Appointment(
            id=appointment_id,
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=7),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status=AppointmentStatus.IN_PROGRESS,
            notes=None,
            total_price=0.0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = appointment
        mock_repo.save.side_effect = lambda a: a

        # Act
        response = await use_case.mark_no_show(appointment_id)

        # Assert
        assert response.status == AppointmentStatus.NO_SHOW
        mock_repo.save.assert_called_once()
