"""API handler for appointment endpoints.

This module provides the FastAPI router for appointment operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.appointments.create_appointment_request import (
    CreateAppointmentRequest,
)
from application.dto.requests.appointments.update_appointment_details_request import (
    UpdateAppointmentDetailsRequest,
)
from application.dto.responses.appointments.appointment_response import (
    AppointmentResponse,
)
from application.use_cases.appointments.appointment_use_case import (
    AppointmentUseCase,
)
from core.container import container
from core.errors import (
    BusinessRuleError,
    EntityNotFoundError,
)
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_appointment_use_case() -> AppointmentUseCase:
    """Dependency injection for the AppointmentUseCase.

    Uses the DI container to resolve the repository implementation.

    Returns:
        An AppointmentUseCase instance.
    """

    return AppointmentUseCase(appointment_repo=container.appointment_repository)


@router.post(
    "/",
    response_model=SuccessResponse[AppointmentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    request: CreateAppointmentRequest,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.CLIENT, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Create a new appointment.

    This endpoint allows clients to book an appointment with an artist.
    The system checks for scheduling conflicts before creating the appointment.

    Args:
        request: Validated appointment creation data.
        use_case: Injected use case for appointment operations.
        current_user: The authenticated user (client or admin).

    Returns:
        A success response containing the created appointment.

    Raises:
        HTTPException: 422 if the artist is not available.
    """

    # Use the authenticated user's ID as the client_id
    client_id = current_user.id

    try:
        appointment = await use_case.create_appointment(client_id, request)

        return SuccessResponse(
            data=appointment,
            message="Appointment created successfully",
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.get(
    "/",
    response_model=SuccessResponse[list[AppointmentResponse]],
)
async def list_appointments(
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[AppointmentResponse]]:
    """List all appointments for the authenticated user.

    Returns the appointments filtered by the user's role:
    - Clients see their own appointments
    - Artists see their appointments
    - Admins see all appointments

    Args:
        use_case: Injected use case for appointment operations.
        current_user: The authenticated user.

    Returns:
        A success response containing a list of appointments.
    """

    # Filter by user role
    if current_user.is_client():
        appointments = await use_case.list_appointments(client_id=current_user.id)
    elif current_user.is_artist():
        appointments = await use_case.list_appointments(artist_id=current_user.id)
    else:
        # Admin sees all appointments
        appointments = await use_case.list_appointments()

    return SuccessResponse(data=appointments)


@router.get(
    "/{appointment_id}",
    response_model=SuccessResponse[AppointmentResponse],
)
async def get_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[AppointmentResponse]:
    """Retrieve an appointment by its unique identifier.

    Args:
        appointment_id: The UUID of the appointment to retrieve.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the appointment data.

    Raises:
        HTTPException: 404 if the appointment is not found.
    """

    try:
        appointment = await use_case.get_appointment(appointment_id)

        return SuccessResponse(data=appointment)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{appointment_id}/accept",
    response_model=SuccessResponse[AppointmentResponse],
)
async def accept_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.ARTIST, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Accept a pending appointment.

    Only the artist or admin can accept an appointment.
    Changes status from PENDING to CONFIRMED.

    Args:
        appointment_id: The UUID of the appointment to accept.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 404 if not found, 422 if transition is invalid.
    """

    try:
        appointment = await use_case.accept_appointment(appointment_id)

        return SuccessResponse(
            data=appointment,
            message="Appointment accepted",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.put(
    "/{appointment_id}/reject",
    response_model=SuccessResponse[AppointmentResponse],
)
async def reject_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.ARTIST, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Reject a pending appointment.

    Only the artist or admin can reject an appointment.
    Changes status from PENDING to CANCELLED.

    Args:
        appointment_id: The UUID of the appointment to reject.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 404 if not found, 422 if transition is invalid.
    """

    try:
        appointment = await use_case.reject_appointment(appointment_id)

        return SuccessResponse(
            data=appointment,
            message="Appointment rejected",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.put(
    "/{appointment_id}/start",
    response_model=SuccessResponse[AppointmentResponse],
)
async def start_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.ARTIST, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Start a confirmed appointment.

    Only the artist or admin can start an appointment.
    Changes status from CONFIRMED to IN_PROGRESS.

    Args:
        appointment_id: The UUID of the appointment to start.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 404 if not found, 422 if transition is invalid.
    """

    try:
        appointment = await use_case.start_appointment(appointment_id)

        return SuccessResponse(
            data=appointment,
            message="Appointment started",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.put(
    "/{appointment_id}/cancel",
    response_model=SuccessResponse[AppointmentResponse],
)
async def cancel_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.CLIENT, UserRole.ARTIST, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Cancel a pending or confirmed appointment.

    Clients can cancel their own appointments.
    Artists and admins can cancel any appointment.
    Changes status to CANCELLED.

    Args:
        appointment_id: The UUID of the appointment to cancel.
        use_case: Injected use case for appointment operations.
        current_user: The authenticated user.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 403 if a client attempts to cancel another user's appointment.
        HTTPException: 404 if not found.
        HTTPException: 422 if transition is invalid.
    """

    try:
        if current_user.is_client():
            appointment = await use_case.get_appointment(appointment_id)
            if appointment.client_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Clients can only cancel their own appointments",
                )

        appointment = await use_case.cancel_appointment(appointment_id)

        return SuccessResponse(
            data=appointment,
            message="Appointment cancelled",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.put(
    "/{appointment_id}/complete",
    response_model=SuccessResponse[AppointmentResponse],
)
async def complete_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.ARTIST, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Complete an in-progress appointment.

    Only the artist or admin can complete an appointment.
    Changes status from IN_PROGRESS to COMPLETED.

    Args:
        appointment_id: The UUID of the appointment to complete.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 404 if not found, 422 if transition is invalid.
    """

    try:
        appointment = await use_case.complete_appointment(appointment_id)

        return SuccessResponse(
            data=appointment,
            message="Appointment completed",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.patch(
    "/{appointment_id}",
    response_model=SuccessResponse[AppointmentResponse],
)
async def update_appointment(
    appointment_id: UUID,
    request: UpdateAppointmentDetailsRequest,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.CLIENT, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Update appointment details (date, time, notes, price).

    Only PENDING or CONFIRMED appointments can be updated.

    Args:
        appointment_id: The UUID of the appointment to update.
        request: Validated update data.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 404 if not found, 422 if update is invalid.
    """

    try:
        if current_user.is_client():
            appointment = await use_case.get_appointment(appointment_id)
            if appointment.client_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Clients can only update their own appointments",
                )

        appointment = await use_case.update_appointment_details(appointment_id, request)

        return SuccessResponse(
            data=appointment,
            message="Appointment updated successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.delete(
    "/{appointment_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
)
async def delete_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[None]:
    """Delete an appointment.

    Only PENDING or CANCELLED appointments can be deleted.

    Args:
        appointment_id: The UUID of the appointment to delete.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response with no data.

    Raises:
        HTTPException: 404 if not found, 422 if deletion is not allowed.
    """

    try:
        await use_case.delete_appointment(appointment_id)

        return SuccessResponse(
            data=None,
            message="Appointment deleted successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.put(
    "/{appointment_id}/no-show",
    response_model=SuccessResponse[AppointmentResponse],
)
async def mark_no_show_appointment(
    appointment_id: UUID,
    use_case: AppointmentUseCase = Depends(get_appointment_use_case),
    current_user: User = Depends(require_role(UserRole.ARTIST, UserRole.ADMIN)),
) -> SuccessResponse[AppointmentResponse]:
    """Mark an appointment as no-show.

    Only the artist or admin can mark as no-show.
    Changes status from IN_PROGRESS to NO_SHOW.

    Args:
        appointment_id: The UUID of the appointment.
        use_case: Injected use case for appointment operations.

    Returns:
        A success response containing the updated appointment.

    Raises:
        HTTPException: 404 if not found, 422 if transition is invalid.
    """

    try:
        appointment = await use_case.mark_no_show(appointment_id)

        return SuccessResponse(
            data=appointment,
            message="Appointment marked as no-show",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )
