"""Appointment repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any appointment repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/supabase/appointment_repository.py
"""

from datetime import date, time
from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus


@runtime_checkable
class AppointmentRepository(Protocol):
    """Interface for Appointment persistence.

    This protocol defines the contract that any appointment repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer by the Supabase repository.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, appointment_id: UUID) -> Appointment | None:
        """Retrieve an appointment by its unique identifier.

        Args:
            appointment_id: The UUID of the appointment to find.

        Returns:
            The Appointment entity if found, None otherwise.
        """
        ...

    async def save(self, appointment: Appointment) -> Appointment:
        """Persist an appointment entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            appointment: The Appointment entity to persist.

        Returns:
            The persisted Appointment entity.
        """
        ...

    async def find_by_artist_and_date(
        self,
        artist_id: UUID,
        appointment_date: date,
        start_time: time,
    ) -> Appointment | None:
        """Find an existing appointment for an artist at a specific time.

        Used to check for scheduling conflicts before creating new appointments.

        Args:
            artist_id: The UUID of the artist.
            appointment_date: The date to check.
            start_time: The start time to check.

        Returns:
            The conflicting Appointment if found, None otherwise.
        """
        ...

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
        ...

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
        ...

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
        ...

    async def delete(self, appointment_id: UUID) -> None:
        """Remove an appointment by its unique identifier.

        Args:
            appointment_id: The UUID of the appointment to delete.
        """
        ...
