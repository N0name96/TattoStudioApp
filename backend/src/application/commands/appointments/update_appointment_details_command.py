"""Command to update appointment details in the TattoStudioApp.

This command handles updating mutable fields of an appointment:
- Date, start time, notes, total price
Only PENDING or CONFIRMED appointments can be updated.
"""

import logging
from uuid import UUID

from application.dto.requests.appointments.update_appointment_details_request import (
    UpdateAppointmentDetailsRequest,
)
from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)


class UpdateAppointmentDetailsCommand:
    """Command to update appointment details.

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
        appointment_id: UUID,
        request: UpdateAppointmentDetailsRequest,
    ) -> AppointmentResponse:
        """Execute the update details flow.

        Steps:
            1. Find the appointment by ID.
            2. Update details (entity validates business rules).
            3. Persist the changes.
            4. Return the updated appointment.

        Args:
            appointment_id: UUID of the appointment to update.
            request: Validated update data.

        Returns:
            The updated appointment as a response DTO.

        Raises:
            EntityNotFoundError: If the appointment does not exist.
            BusinessRuleError: If status doesn't allow updates.
        """

        logger.info(
            "Updating appointment details",
            extra={
                "extra_data": {
                    "appointment_id": str(appointment_id),
                }
            },
        )

        # Step 1: Find the appointment
        appointment = await self._appointment_repo.get_by_id(appointment_id)

        if appointment is None:
            raise EntityNotFoundError(f"Appointment {appointment_id} not found")

        # Step 2: Update details (entity validates business rules)
        appointment.update_details(
            appointment_date=request.date,
            start_time=request.start_time,
            notes=request.notes,
            total_price=request.total_price,
        )

        # Step 3: Persist the changes
        saved = await self._appointment_repo.save(appointment)

        logger.info(
            "Appointment details updated",
            extra={
                "extra_data": {
                    "appointment_id": str(saved.id),
                }
            },
        )

        # Step 4: Return the updated appointment
        return AppointmentResponse.model_validate(saved)
