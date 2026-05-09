"""Command to update an appointment's status in the TattoStudioApp.

This command handles status transitions for appointments:
- Accept (PENDING -> CONFIRMED)
- Reject (PENDING -> CANCELLED)
- Start (CONFIRMED -> IN_PROGRESS)
- Complete (IN_PROGRESS -> COMPLETED)
- Cancel (PENDING/CONFIRMED -> CANCELLED)
- Mark no-show (IN_PROGRESS -> NO_SHOW)
"""

import logging
from uuid import UUID

from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)

# Map of status names to entity methods
STATUS_ACTIONS: dict[str, str] = {
    "accept": "accept",
    "reject": "reject",
    "start": "start",
    "complete": "complete",
    "cancel": "cancel",
    "no_show": "mark_no_show",
}


class UpdateAppointmentStatusCommand:
    """Command to update an appointment's status.

    This command finds an appointment by ID and applies the requested
    status transition. The entity validates whether the transition
    is allowed according to business rules.

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
        action: str,
    ) -> AppointmentResponse:
        """Execute the status update flow.

        Steps:
            1. Find the appointment by ID.
            2. Apply the requested status transition.
            3. Persist the changes.
            4. Return the updated appointment.

        Args:
            appointment_id: UUID of the appointment to update.
            action: The action to perform (accept, reject, start, complete, cancel, no_show).

        Returns:
            The updated appointment as a response DTO.

        Raises:
            EntityNotFoundError: If the appointment does not exist.
            BusinessRuleError: If the transition is not allowed.
            ValueError: If the action is not valid.
        """

        logger.info(
            "Updating appointment status",
            extra={
                "extra_data": {
                    "appointment_id": str(appointment_id),
                    "action": action,
                }
            },
        )

        # Validate action
        if action not in STATUS_ACTIONS:
            raise ValueError(
                f"Invalid action: {action}. Valid actions: {list(STATUS_ACTIONS.keys())}"
            )

        # Step 1: Find the appointment
        appointment = await self._appointment_repo.get_by_id(appointment_id)

        if appointment is None:
            raise EntityNotFoundError(f"Appointment {appointment_id} not found")

        # Step 2: Apply the status transition
        method_name = STATUS_ACTIONS[action]
        method = getattr(appointment, method_name)
        method()

        # Step 3: Persist the changes
        saved = await self._appointment_repo.save(appointment)

        logger.info(
            "Appointment status updated",
            extra={
                "extra_data": {
                    "appointment_id": str(saved.id),
                    "new_status": saved.status.value,
                }
            },
        )

        # Step 4: Return the updated appointment
        return AppointmentResponse.model_validate(saved)
