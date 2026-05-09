"""Query to retrieve a single appointment by ID.

This query handles the read operation for appointment data,
mapping from domain entity to response DTO.
"""

import logging
from uuid import UUID

from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)


class GetAppointmentQuery:
    """Query to retrieve a single appointment by ID.

    This query handles the read operation for appointment data,
    mapping from domain entity to response DTO.

    Attributes:
        _appointment_repo: Repository for appointment lookups.
    """

    def __init__(self, appointment_repo: AppointmentRepository) -> None:
        """Initialize the query with the appointment repository.

        Args:
            appointment_repo: Repository for appointment lookups.
        """

        self._appointment_repo = appointment_repo

    async def execute(self, appointment_id: UUID) -> AppointmentResponse:
        """Execute the appointment retrieval.

        Args:
            appointment_id: The unique identifier of the appointment.

        Returns:
            The appointment data as a response DTO.

        Raises:
            EntityNotFoundError: If the appointment does not exist.
        """

        logger.debug(
            "Retrieving appointment",
            extra={"extra_data": {"appointment_id": str(appointment_id)}},
        )

        appointment = await self._appointment_repo.get_by_id(appointment_id)

        if appointment is None:
            raise EntityNotFoundError(f"Appointment {appointment_id} not found")

        return AppointmentResponse.model_validate(appointment)
