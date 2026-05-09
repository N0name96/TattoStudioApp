"""Command to delete an appointment in the TattoStudioApp.

This command handles appointment deletion with business rules:
- Only PENDING or CANCELLED appointments can be deleted.
"""

import logging
from uuid import UUID

from core.errors import EntityNotFoundError
from domain.repositories.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)


class DeleteAppointmentCommand:
    """Command to delete an appointment.

    Attributes:
        _appointment_repo: Repository for appointment persistence.
    """

    def __init__(self, appointment_repo: AppointmentRepository) -> None:
        """Initialize the command with the appointment repository.

        Args:
            appointment_repo: Repository for appointment persistence.
        """

        self._appointment_repo = appointment_repo

    async def execute(self, appointment_id: UUID) -> None:
        """Execute the delete flow.

        Steps:
            1. Find the appointment by ID.
            2. Validate deletion is allowed.
            3. Delete the appointment.

        Args:
            appointment_id: UUID of the appointment to delete.

        Raises:
            EntityNotFoundError: If the appointment does not exist.
            BusinessRuleError: If appointment cannot be deleted.
        """

        logger.info(
            "Deleting appointment",
            extra={"extra_data": {"appointment_id": str(appointment_id)}},
        )

        # Step 1: Find the appointment
        appointment = await self._appointment_repo.get_by_id(appointment_id)

        if appointment is None:
            raise EntityNotFoundError(f"Appointment {appointment_id} not found")

        # Step 2: Validate deletion is allowed (entity enforces business rule)
        appointment.delete()

        # Step 3: Delete
        await self._appointment_repo.delete(appointment_id)

        logger.info(
            "Appointment deleted",
            extra={"extra_data": {"appointment_id": str(appointment_id)}},
        )
