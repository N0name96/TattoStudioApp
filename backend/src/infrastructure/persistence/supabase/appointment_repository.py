"""Supabase implementation of the AppointmentRepository.

This module provides the concrete persistence layer for Appointment
entities, translating domain operations into Supabase queries.

Implements the AppointmentRepository Protocol defined in the Domain layer.
"""

import logging
from datetime import date, time
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import (
    map_to_appointment,
    map_to_appointment_dict,
)

logger = logging.getLogger(__name__)


class SupabaseAppointmentRepository:
    """Implements AppointmentRepository Protocol using Supabase.

    This class provides the concrete persistence layer for Appointment
    entities, translating domain operations into Supabase queries.

    Attributes:
        TABLE: The Supabase table name for appointments.
    """

    TABLE = "appointments"

    async def get_by_id(self, appointment_id: UUID) -> Appointment | None:
        """Retrieve an appointment by its unique ID.

        Args:
            appointment_id: The UUID of the appointment to find.

        Returns:
            The Appointment entity if found, None otherwise.

        Raises:
            DatabaseError: If the query fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()

            response = client.table(self.TABLE).select("*").eq("id", str(appointment_id)).execute()

            if not response.data:
                return None

            return map_to_appointment(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get appointment: {e}")

    async def save(self, appointment: Appointment) -> Appointment:
        """Persist an appointment entity (create or update).

        Uses upsert to handle both creation and updates.

        Args:
            appointment: The Appointment entity to persist.

        Returns:
            The persisted Appointment entity.

        Raises:
            DatabaseError: If the operation fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()
            data = map_to_appointment_dict(appointment)

            response = client.table(self.TABLE).upsert(data).execute()

            if not response.data:
                raise DatabaseError("Failed to save appointment: no data returned")

            return map_to_appointment(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save appointment: {e}")

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

        Raises:
            DatabaseError: If the query fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()

            response = (
                client.table(self.TABLE)
                .select("*")
                .eq("artist_id", str(artist_id))
                .eq("date", appointment_date.isoformat())
                .eq("start_time", start_time.isoformat())
                .not_.in_("status", ["cancelled", "no_show"])
                .execute()
            )

            if not response.data:
                return None

            return map_to_appointment(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to find appointment: {e}")

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

        Raises:
            DatabaseError: If the query fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*").eq("client_id", str(client_id))

            if status is not None:
                query = query.eq("status", status.value)

            response = query.order("date", desc=False).execute()

            return [map_to_appointment(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list appointments: {e}")

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

        Raises:
            DatabaseError: If the query fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*").eq("artist_id", str(artist_id))

            if status is not None:
                query = query.eq("status", status.value)

            response = query.order("date", desc=False).execute()

            return [map_to_appointment(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list appointments: {e}")

    async def list_all(
        self,
        status: AppointmentStatus | None = None,
    ) -> list[Appointment]:
        """List all appointments in the system (admin view).

        Args:
            status: Optional filter by appointment status.

        Returns:
            A list of all Appointment entities.

        Raises:
            DatabaseError: If the query fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*")

            if status is not None:
                query = query.eq("status", status.value)

            response = query.order("date", desc=False).execute()

            return [map_to_appointment(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list appointments: {e}")

    async def delete(self, appointment_id: UUID) -> None:
        """Remove an appointment by its unique identifier.

        Args:
            appointment_id: The UUID of the appointment to delete.

        Raises:
            DatabaseError: If the operation fails.
        """

        try:
            client = await SupabaseClientSingleton.get_client()
            client.table(self.TABLE).delete().eq("id", str(appointment_id)).execute()
        except Exception as e:
            raise DatabaseError(f"Failed to delete appointment: {e}")
