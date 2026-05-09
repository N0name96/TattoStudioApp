"""API handler for payment endpoints.

This module provides the FastAPI router for payment operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.payments.create_payment_request import (
    CreatePaymentRequest,
)
from application.dto.responses.payments.payment_response import (
    PaymentResponse,
)
from application.use_cases.payments.payment_use_case import (
    PaymentUseCase,
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

router = APIRouter(prefix="/payments", tags=["payments"])


def get_payment_use_case() -> PaymentUseCase:
    """Dependency injection for the PaymentUseCase.

    Uses the DI container to resolve the repository implementations.

    Returns:
        A PaymentUseCase instance.
    """

    return PaymentUseCase(
        payment_repo=container.payment_repository,
        appointment_repo=container.appointment_repository,
    )


@router.post(
    "/",
    response_model=SuccessResponse[PaymentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    request: CreatePaymentRequest,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
    current_user: User = Depends(require_role(UserRole.CLIENT, UserRole.ADMIN)),
) -> SuccessResponse[PaymentResponse]:
    """Create a new payment for an appointment.

    This endpoint allows clients to initiate a payment for a
    booked appointment.

    Args:
        request: Validated payment creation data.
        use_case: Injected use case for payment operations.
        current_user: The authenticated user.

    Returns:
        A success response containing the created payment.

    Raises:
        HTTPException: 404 if the appointment does not exist.
        HTTPException: 422 if the payment amount is invalid.
    """

    try:
        payment = await use_case.create_payment(request)

        return SuccessResponse(data=payment, message="Payment created successfully")

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e

    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        ) from e


@router.get(
    "/{payment_id}",
    response_model=SuccessResponse[PaymentResponse],
)
async def get_payment(
    payment_id: UUID,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[PaymentResponse]:
    """Retrieve a payment by its unique identifier.

    Args:
        payment_id: The UUID of the payment to retrieve.
        use_case: Injected use case for payment operations.
        current_user: The authenticated user.

    Returns:
        A success response containing the payment data.

    Raises:
        HTTPException: 404 if the payment is not found.
    """

    try:
        payment = await use_case.get_payment(payment_id)

        return SuccessResponse(data=payment)

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e


@router.get(
    "/",
    response_model=SuccessResponse[list[PaymentResponse]],
)
async def list_payments(
    appointment_id: UUID | None = None,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[PaymentResponse]]:
    """List payments with optional filters.

    Args:
        appointment_id: Optional filter by appointment UUID.
        use_case: Injected use case for payment operations.
        current_user: The authenticated user.

    Returns:
        A success response containing a list of payments.
    """

    payments = await use_case.list_payments(appointment_id=appointment_id)

    return SuccessResponse(data=payments)


@router.post(
    "/{payment_id}/refund",
    response_model=SuccessResponse[PaymentResponse],
)
async def refund_payment(
    payment_id: UUID,
    use_case: PaymentUseCase = Depends(get_payment_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[PaymentResponse]:
    """Refund a completed payment (admin only).

    Args:
        payment_id: The UUID of the payment to refund.
        use_case: Injected use case for payment operations.
        current_user: The authenticated admin user.

    Returns:
        A success response containing the refunded payment.

    Raises:
        HTTPException: 404 if the payment is not found.
        HTTPException: 422 if the payment cannot be refunded.
    """

    try:
        payment = await use_case.refund_payment(payment_id)

        return SuccessResponse(data=payment, message="Payment refunded successfully")

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e

    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        ) from e
