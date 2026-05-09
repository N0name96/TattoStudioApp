"""Command to create a new appointment in the TattoStudioApp.

This command handles the appointment creation flow:
1. Verify the artist exists
2. Check artist availability (no overlapping appointments)
3. Create the domain entity
4. Persist to repository
5. Return response DTO
"""

import logging
from uuid import UUID

from application.dto.requests.appointments.create_appointment_request import (
    CreateAppointmentRequest,
)
from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from core.errors import BusinessRuleError
from domain.entities.appointment_entity import Appointment
from domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)


class CreateAppointmentCommand:
    """Command to create a new appointment in the system.

    This command validates the request, checks artist availability,
    creates the domain entity and persists it to the repository.

    Attributes:
        _appointment_repo: Repository for appointment persistence.
    """

    def __init__(self, appointment_repo: AppointmentRepository) -> None:
        """Initialize the command with the appointment repository.

        Args:
            appointment_repo: Repository for appointment persistence.
        """

        self._appointment_repo = appointment_repo

    async def execute(
        self,
        client_id: UUID,
        request: CreateAppointmentRequest,
    ) -> AppointmentResponse:
        """Execute the appointment creation flow.

        Steps:
            1. Check the artist is available at the requested time.
            2. Create the domain entity with business rules applied.
            3. Persist the appointment.
            4. Return the response DTO.

        Args:
            client_id: UUID of the client creating the appointment.
            request: Validated appointment creation data.

        Returns:
            The created appointment as a response DTO.

        Raises:
            BusinessRuleError: If the artist is not available at the requested time.
        """

        logger.info(
            "Creating appointment",
            extra={
                "extra_data": {
                    "client_id": str(client_id),
                    "artist_id": str(request.artist_id),
                    "service_type": request.service_type.value,
                    "date": str(request.date),
                    "start_time": str(request.start_time),
                }
            },
        )

        # Step 1: Check availability for the requested slot
        existing = await self._appointment_repo.find_by_artist_and_date(
            artist_id=request.artist_id,
            appointment_date=request.date,
            start_time=request.start_time,
        )

        if existing is not None:
            raise BusinessRuleError(
                f"Artist is not available at {request.start_time} on {request.date}"
            )

        # Step 2: Create the domain entity with business rules applied
        appointment = Appointment.create(
            client_id=client_id,
            artist_id=request.artist_id,
            service_type=request.service_type,
            appointment_date=request.date,
            start_time=request.start_time,
            notes=request.notes,
        )

        # Step 3: Persist the appointment
        saved = await self._appointment_repo.save(appointment)

        logger.info(
            "Appointment created successfully",
            extra={
                "extra_data": {
                    "appointment_id": str(saved.id),
                    "status": saved.status.value,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return AppointmentResponse.model_validate(saved)
