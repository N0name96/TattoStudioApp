"""In-memory mock implementation of the AppointmentRepository.

This module provides a non-persistent repository for development
and testing purposes. Data is stored in memory and lost on restart.

Usage:
    from infrastructure.persistence.in_memory.appointment_repository import (
        InMemoryAppointmentRepository,
    )
    repo = InMemoryAppointmentRepository()
"""

import logging
from datetime import date, time
from uuid import UUID

from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus

logger = logging.getLogger(__name__)


class InMemoryAppointmentRepository:
    """In-memory implementation of the AppointmentRepository.

    Stores appointments in a dictionary for development and testing.
    Data is lost when the application restarts.

    Attributes:
        _storage: Dictionary mapping appointment IDs to entities.
    """

    def __init__(self) -> None:
        """Initialize the in-memory storage."""

        self._storage: dict[UUID, Appointment] = {}

        logger.info("InMemoryAppointmentRepository initialized")

    async def get_by_id(self, appointment_id: UUID) -> Appointment | None:
        """Retrieve an appointment by its unique ID.

        Args:
            appointment_id: The UUID of the appointment to find.

        Returns:
            The Appointment entity if found, None otherwise.
        """

        return self._storage.get(appointment_id)

    async def save(self, appointment: Appointment) -> Appointment:
        """Persist an appointment entity (create or update).

        Args:
            appointment: The Appointment entity to persist.

        Returns:
            The persisted Appointment entity.
        """

        self._storage[appointment.id] = appointment

        logger.debug(
            "Appointment saved",
            extra={"extra_data": {"appointment_id": str(appointment.id)}},
        )

        return appointment

    async def find_by_artist_and_date(
        self,
        artist_id: UUID,
        appointment_date: date,
        start_time: time,
    ) -> Appointment | None:
        """Find an existing appointment for an artist at a specific time.

        Args:
            artist_id: The UUID of the artist.
            appointment_date: The date to check.
            start_time: The start time to check.

        Returns:
            The conflicting Appointment if found, None otherwise.
        """

        for appointment in self._storage.values():
            if (
                appointment.artist_id == artist_id
                and appointment.date == appointment_date
                and appointment.start_time == start_time
                and appointment.status
                not in [
                    AppointmentStatus.CANCELLED,
                    AppointmentStatus.NO_SHOW,
                ]
            ):
                return appointment

        return None

    async def list_by_client(
        self,
        client_id: UUID,
        status: AppointmentStatus | None = None,
    ) -> list[Appointment]:
        """List all appointments for a specific client.

        Args:
            client_id: The UUID of the client.
            status: Optional filter by appointment status.

        Returns:
            A list of Appointment entities for the client.
        """

        results = [a for a in self._storage.values() if a.client_id == client_id]

        if status is not None:
            results = [a for a in results if a.status == status]

        return sorted(results, key=lambda a: a.date)

    async def list_by_artist(
        self,
        artist_id: UUID,
        status: AppointmentStatus | None = None,
    ) -> list[Appointment]:
        """List all appointments for a specific artist.

        Args:
            artist_id: The UUID of the artist.
            status: Optional filter by appointment status.

        Returns:
            A list of Appointment entities for the artist.
        """

        results = [a for a in self._storage.values() if a.artist_id == artist_id]

        if status is not None:
            results = [a for a in results if a.status == status]

        return sorted(results, key=lambda a: a.date)

    async def list_all(
        self,
        status: AppointmentStatus | None = None,
    ) -> list[Appointment]:
        """List all appointments in the system (admin view).

        Args:
            status: Optional filter by appointment status.

        Returns:
            A list of all Appointment entities.
        """

        results = list(self._storage.values())

        if status is not None:
            results = [a for a in results if a.status == status]

        return sorted(results, key=lambda a: a.date)

    async def delete(self, appointment_id: UUID) -> None:
        """Remove an appointment by its unique identifier.

        Args:
            appointment_id: The UUID of the appointment to delete.
        """

        self._storage.pop(appointment_id, None)
