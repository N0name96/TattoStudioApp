"""Tests for the GetAppointmentQuery.

This module tests the appointment retrieval logic with mocked repositories
to isolate the query logic from infrastructure dependencies.
"""

from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.queries.appointments.get_appointment_query import (
    GetAppointmentQuery,
)
from core.errors import EntityNotFoundError
from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


@pytest.fixture
def mock_repo():
    """Create a mock appointment repository."""

    repo = AsyncMock()
    return repo


@pytest.fixture
def sample_appointment():
    """Create a sample appointment for testing."""

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


class TestGetAppointmentQuery:
    """Tests for GetAppointmentQuery.execute()."""

    @pytest.mark.asyncio
    async def test_get_appointment_success(self, mock_repo, sample_appointment):
        """Test successful appointment retrieval."""

        # Arrange
        mock_repo.get_by_id.return_value = sample_appointment

        query = GetAppointmentQuery(mock_repo)

        # Act
        response = await query.execute(sample_appointment.id)

        # Assert
        assert response.id == sample_appointment.id
        assert response.client_id == sample_appointment.client_id
        assert response.artist_id == sample_appointment.artist_id
        assert response.status == AppointmentStatus.PENDING
        mock_repo.get_by_id.assert_called_once_with(sample_appointment.id)

    @pytest.mark.asyncio
    async def test_get_appointment_raises_entity_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised when appointment not found."""

        # Arrange
        mock_repo.get_by_id.return_value = None

        query = GetAppointmentQuery(mock_repo)

        # Act & Assert
        with pytest.raises(EntityNotFoundError):
            await query.execute(uuid4())

    @pytest.mark.asyncio
    async def test_get_appointment_returns_response_dto(self, mock_repo, sample_appointment):
        """Test that the response is a proper AppointmentResponse DTO."""

        # Arrange
        mock_repo.get_by_id.return_value = sample_appointment

        query = GetAppointmentQuery(mock_repo)

        # Act
        response = await query.execute(sample_appointment.id)

        # Assert
        assert hasattr(response, "model_dump")
        assert response.service_type == ServiceType.TATTOO
        assert response.total_price == 100.0
