"""Use case for appointment operations in the TattoStudioApp.

This module provides a high-level interface for appointment operations,
orchestrating commands and queries. It acts as the entry point for
the API layer to interact with the appointments domain.
"""

from uuid import UUID

from application.commands.appointments.create_appointment_command import (
    CreateAppointmentCommand,
)
from application.commands.appointments.delete_appointment_command import (
    DeleteAppointmentCommand,
)
from application.commands.appointments.update_appointment_details_command import (
    UpdateAppointmentDetailsCommand,
)
from application.commands.appointments.update_appointment_status_command import (
    UpdateAppointmentStatusCommand,
)
from application.dto.requests.appointments.create_appointment_request import (
    CreateAppointmentRequest,
)
from application.dto.requests.appointments.update_appointment_details_request import (
    UpdateAppointmentDetailsRequest,
)
from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from application.queries.appointments.get_appointment_query import (
    GetAppointmentQuery,
)
from application.queries.appointments.list_appointments_query import (
    ListAppointmentsQuery,
)
from domain.enums.appointment_status import AppointmentStatus
from domain.repositories.appointment_repository import AppointmentRepository


class AppointmentUseCase:
    """Use case for appointment operations.

    Orchestrates commands and queries for the appointments module.
    Provides a single entry point for the API layer.

    Attributes:
        _appointment_repo: Repository for appointment persistence.
        _create_command: Command for creating appointments.
        _update_status_command: Command for updating appointment status.
        _get_query: Query for retrieving a single appointment.
        _list_query: Query for listing appointments.
    """

    def __init__(self, appointment_repo: AppointmentRepository) -> None:
        """Initialize the use case with the appointment repository.

        Args:
            appointment_repo: Repository for appointment persistence.
        """

        self._appointment_repo = appointment_repo
        self._create_command = CreateAppointmentCommand(appointment_repo)
        self._update_status_command = UpdateAppointmentStatusCommand(appointment_repo)
        self._update_details_command = UpdateAppointmentDetailsCommand(appointment_repo)
        self._delete_command = DeleteAppointmentCommand(appointment_repo)
        self._get_query = GetAppointmentQuery(appointment_repo)
        self._list_query = ListAppointmentsQuery(appointment_repo)

    async def create_appointment(
        self,
        client_id: UUID,
        request: CreateAppointmentRequest,
    ) -> AppointmentResponse:
        """Create a new appointment.

        Args:
            client_id: UUID of the client creating the appointment.
            request: Validated appointment creation data.

        Returns:
            The created appointment as a response DTO.
        """

        return await self._create_command.execute(client_id, request)

    async def get_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        """Retrieve a single appointment by ID.

        Args:
            appointment_id: UUID of the appointment to retrieve.

        Returns:
            The appointment as a response DTO.
        """

        return await self._get_query.execute(appointment_id)

    async def list_appointments(
        self,
        client_id: UUID | None = None,
        artist_id: UUID | None = None,
        status: AppointmentStatus | None = None,
    ) -> list[AppointmentResponse]:
        """List appointments with optional filters.

        Args:
            client_id: Optional filter by client UUID.
            artist_id: Optional filter by artist UUID.
            status: Optional filter by appointment status.

        Returns:
            A list of appointment response DTOs.
        """

        return await self._list_query.execute(
            client_id=client_id,
            artist_id=artist_id,
            status=status,
        )

    async def accept_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        """Accept a pending appointment.

        Args:
            appointment_id: UUID of the appointment to accept.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_status_command.execute(appointment_id, "accept")

    async def reject_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        """Reject a pending appointment.

        Args:
            appointment_id: UUID of the appointment to reject.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_status_command.execute(appointment_id, "reject")

    async def start_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        """Start a confirmed appointment.

        Args:
            appointment_id: UUID of the appointment to start.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_status_command.execute(appointment_id, "start")

    async def complete_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        """Complete an in-progress appointment.

        Args:
            appointment_id: UUID of the appointment to complete.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_status_command.execute(appointment_id, "complete")

    async def cancel_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        """Cancel a pending or confirmed appointment.

        Args:
            appointment_id: UUID of the appointment to cancel.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_status_command.execute(appointment_id, "cancel")

    async def mark_no_show(self, appointment_id: UUID) -> AppointmentResponse:
        """Mark an appointment as no-show.

        Args:
            appointment_id: UUID of the appointment to mark as no-show.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_status_command.execute(appointment_id, "no_show")

    async def update_appointment_details(
        self,
        appointment_id: UUID,
        request: UpdateAppointmentDetailsRequest,
    ) -> AppointmentResponse:
        """Update appointment details.

        Args:
            appointment_id: UUID of the appointment to update.
            request: Validated update data.

        Returns:
            The updated appointment as a response DTO.
        """

        return await self._update_details_command.execute(appointment_id, request)

    async def delete_appointment(self, appointment_id: UUID) -> None:
        """Delete an appointment.

        Args:
            appointment_id: UUID of the appointment to delete.
        """

        await self._delete_command.execute(appointment_id)
