"""API handler for cash transaction endpoints.

This module provides the FastAPI router for cash transaction operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).
"""

import logging
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.cash.create_cash_transaction_request import (
    CreateCashTransactionRequest,
)
from application.dto.responses.cash.cash_transaction_response import (
    CashTransactionResponse,
)
from application.use_cases.cash.cash_use_case import CashUseCase
from core.container import container
from core.errors import EntityNotFoundError
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.cash_transaction_type import CashTransactionType
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cash", tags=["cash"])


def get_cash_use_case() -> CashUseCase:
    """Provide the CashUseCase dependency for cash endpoints.

    The use case is resolved from the application container and encapsulates
    the cash transaction business logic for create/read/delete operations.

    Returns:
        A CashUseCase instance.
    """

    return CashUseCase(cash_repo=container.cash_repository)


@router.post(
    "/",
    response_model=SuccessResponse[CashTransactionResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    request: CreateCashTransactionRequest,
    use_case: CashUseCase = Depends(get_cash_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[CashTransactionResponse]:
    """Create a new cash transaction.

    Only admins can create cash transactions.

    Args:
        request: Validated cash transaction creation data.
        use_case: Injected use case for cash operations.
        current_user: Authenticated admin user.

    Returns:
        A success response containing the created transaction.

    Raises:
        HTTPException: 422 if validation fails.
    """

    transaction = await use_case.create_transaction(request)
    return SuccessResponse(
        data=transaction,
        message="Cash transaction created successfully",
    )


@router.get(
    "/",
    response_model=SuccessResponse[list[CashTransactionResponse]],
)
async def list_transactions(
    transaction_type: CashTransactionType | None = Query(default=None),
    performed_by: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    use_case: CashUseCase = Depends(get_cash_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[CashTransactionResponse]]:
    """List cash transactions with optional filters.

    All authenticated users can list transactions.

    Args:
        transaction_type: Optional filter by transaction type.
        performed_by: Optional filter by user who performed the transaction.
        date_from: Optional filter for transactions on or after this date.
        date_to: Optional filter for transactions on or before this date.
        use_case: Injected use case for cash operations.
        current_user: Authenticated user.

    Returns:
        A success response containing a list of transactions.
    """

    transactions = await use_case.list_transactions(
        transaction_type=transaction_type,
        performed_by=performed_by,
        date_from=date_from,
        date_to=date_to,
    )
    return SuccessResponse(data=transactions)


@router.get(
    "/{transaction_id}",
    response_model=SuccessResponse[CashTransactionResponse],
)
async def get_transaction(
    transaction_id: UUID,
    use_case: CashUseCase = Depends(get_cash_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[CashTransactionResponse]:
    """Retrieve a cash transaction by its unique identifier.

    Args:
        transaction_id: The UUID of the transaction to retrieve.
        use_case: Injected use case for cash operations.
        current_user: Authenticated user.

    Returns:
        A success response containing the transaction data.

    Raises:
        HTTPException: 404 if the transaction is not found.
    """

    try:
        transaction = await use_case.get_transaction(transaction_id)
        return SuccessResponse(data=transaction)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete(
    "/{transaction_id}",
    response_model=SuccessResponse[None],
)
async def delete_transaction(
    transaction_id: UUID,
    use_case: CashUseCase = Depends(get_cash_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[None]:
    """Delete a cash transaction.

    Only admins can delete cash transactions.

    Args:
        transaction_id: The UUID of the transaction to delete.
        use_case: Injected use case for cash operations.
        current_user: Authenticated admin user.

    Returns:
        A success response with no data.

    Raises:
        HTTPException: 404 if the transaction is not found.
    """

    try:
        await use_case.delete_transaction(transaction_id)
        return SuccessResponse(
            data=None,
            message="Cash transaction deleted successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
