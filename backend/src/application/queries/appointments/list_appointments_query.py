"""Query to list appointments with optional filters.

This query handles listing appointments for clients, artists, or admins
with optional status filtering.
"""

import logging
from uuid import UUID

from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from domain.enums.appointment_status import AppointmentStatus
from domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)


class ListAppointmentsQuery:
    """Query to list appointments with optional filters.

    Supports filtering by:
    - Client ID (for client's own appointments)
    - Artist ID (for artist's appointments)
    - Status (pending, confirmed, completed, etc.)

    Attributes:
        _appointment_repo: Repository for appointment lookups.
    """

    def __init__(self, appointment_repo: AppointmentRepository) -> None:
        """Initialize the query with the appointment repository.

        Args:
            appointment_repo: Repository for appointment lookups.
        """

        self._appointment_repo = appointment_repo

    async def execute(
        self,
        client_id: UUID | None = None,
        artist_id: UUID | None = None,
        status: AppointmentStatus | None = None,
    ) -> list[AppointmentResponse]:
        """Execute the appointment listing.

        Filters are applied based on which parameters are provided:
        - If client_id is set: returns client's appointments
        - If artist_id is set: returns artist's appointments
        - If neither is set: returns all appointments (admin view)

        Args:
            client_id: Optional filter by client UUID.
            artist_id: Optional filter by artist UUID.
            status: Optional filter by appointment status.

        Returns:
            A list of appointment response DTOs.
        """

        logger.debug(
            "Listing appointments",
            extra={
                "extra_data": {
                    "client_id": str(client_id) if client_id else None,
                    "artist_id": str(artist_id) if artist_id else None,
                    "status": status.value if status else None,
                }
            },
        )

        # Determine which list method to use based on filters
        if client_id is not None:
            appointments = await self._appointment_repo.list_by_client(
                client_id=client_id,
                status=status,
            )
        elif artist_id is not None:
            appointments = await self._appointment_repo.list_by_artist(
                artist_id=artist_id,
                status=status,
            )
        else:
            appointments = await self._appointment_repo.list_all(
                status=status,
            )

        # Map domain entities to response DTOs
        return [AppointmentResponse.model_validate(a) for a in appointments]
