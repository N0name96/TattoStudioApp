"""Tests for the ListAppointmentsQuery.

This module tests the appointment listing logic with mocked repositories
to isolate the query logic from infrastructure dependencies.
"""


from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.queries.appointments.list_appointments_query import (
    ListAppointmentsQuery,
)
from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


@pytest.fixture
def mock_repo():
    """Create a mock appointment repository."""

    repo = AsyncMock()
    return repo


@pytest.fixture
def sample_appointments():
    """Create a list of sample appointments."""

    now = datetime.now()

    return [
        Appointment(
            id=uuid4(),
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            date=date.today() + timedelta(days=i),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status=AppointmentStatus.PENDING,
            notes=None,
            total_price=100.0,
            created_at=now,
            updated_at=now,
        )
        for i in range(3)
    ]


class TestListAppointmentsQuery:
    """Tests for ListAppointmentsQuery.execute()."""

    @pytest.mark.asyncio
    async def test_list_by_client(self, mock_repo, sample_appointments):
        """Test listing appointments filtered by client."""

        # Arrange
        client_id = uuid4()
        mock_repo.list_by_client.return_value = sample_appointments

        query = ListAppointmentsQuery(mock_repo)

        # Act
        result = await query.execute(client_id=client_id)

        # Assert
        assert len(result) == 3
        mock_repo.list_by_client.assert_called_once_with(
            client_id=client_id,
            status=None,
        )

    @pytest.mark.asyncio
    async def test_list_by_artist(self, mock_repo, sample_appointments):
        """Test listing appointments filtered by artist."""

        # Arrange
        artist_id = uuid4()
        mock_repo.list_by_artist.return_value = sample_appointments

        query = ListAppointmentsQuery(mock_repo)

        # Act
        result = await query.execute(artist_id=artist_id)

        # Assert
        assert len(result) == 3
        mock_repo.list_by_artist.assert_called_once_with(
            artist_id=artist_id,
            status=None,
        )

    @pytest.mark.asyncio
    async def test_list_all(self, mock_repo, sample_appointments):
        """Test listing all appointments (admin view)."""

        # Arrange
        mock_repo.list_all.return_value = sample_appointments

        query = ListAppointmentsQuery(mock_repo)

        # Act
        result = await query.execute()

        # Assert
        assert len(result) == 3
        mock_repo.list_all.assert_called_once_with(status=None)

    @pytest.mark.asyncio
    async def test_list_with_status_filter(self, mock_repo, sample_appointments):
        """Test listing appointments with status filter."""

        # Arrange
        client_id = uuid4()
        mock_repo.list_by_client.return_value = sample_appointments[:1]

        query = ListAppointmentsQuery(mock_repo)

        # Act
        result = await query.execute(
            client_id=client_id,
            status=AppointmentStatus.PENDING,
        )

        # Assert
        assert len(result) == 1
        mock_repo.list_by_client.assert_called_once_with(
            client_id=client_id,
            status=AppointmentStatus.PENDING,
        )

    @pytest.mark.asyncio
    async def test_list_returns_empty_when_no_appointments(self, mock_repo):
        """Test that empty list is returned when no appointments exist."""

        # Arrange
        mock_repo.list_all.return_value = []

        query = ListAppointmentsQuery(mock_repo)

        # Act
        result = await query.execute()

        # Assert
        assert len(result) == 0
