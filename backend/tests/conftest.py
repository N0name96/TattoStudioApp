"""Shared test fixtures for the TattoStudioApp test suite.

This module provides common fixtures used across all test modules,
including mock repositories and sample data.
"""


from datetime import date, time, timedelta
from uuid import UUID, uuid4

import pytest

from core.container import container
from domain.entities.appointment_entity import Appointment
from domain.enums.service_type import ServiceType


@pytest.fixture
def sample_client_id() -> UUID:
    """A sample client UUID for testing."""

    return uuid4()


@pytest.fixture
def sample_artist_id() -> UUID:
    """A sample artist UUID for testing."""

    return uuid4()


@pytest.fixture
def sample_appointment(sample_client_id: UUID, sample_artist_id: UUID) -> Appointment:
    """A sample appointment entity for testing."""

    return Appointment.create(
        client_id=sample_client_id,
        artist_id=sample_artist_id,
        service_type=ServiceType.TATTOO,
        appointment_date=date.today() + timedelta(days=7),
        start_time=time(10, 0),
        notes="Test appointment",
    )


@pytest.fixture
def confirmed_appointment(sample_appointment: Appointment) -> Appointment:
    """A sample confirmed appointment for testing."""

    sample_appointment.accept()
    return sample_appointment


@pytest.fixture
def in_progress_appointment(confirmed_appointment: Appointment) -> Appointment:
    """A sample in-progress appointment for testing."""

    confirmed_appointment.start()
    return confirmed_appointment


@pytest.fixture(autouse=True)
def reset_container() -> None:
    """Reset the DI container between tests to avoid repository state leaking."""

    container._user_repository = None
    container._appointment_repository = None
    container._security_service = None
    yield
    container._user_repository = None
    container._appointment_repository = None
    container._security_service = None
