"""Command to create a cash transaction in the TattoStudioApp.

This command handles the cash transaction creation flow:
1. Create the domain entity
2. Persist to repository
3. Return response DTO
"""

import logging

from application.dto.requests.cash.create_cash_transaction_request import (
    CreateCashTransactionRequest,
)
from application.dto.responses.cash.cash_transaction_response import CashTransactionResponse
from domain.entities.cash_transaction_entity import CashTransaction
from domain.repositories.cash_repository import CashRepository

logger = logging.getLogger(__name__)


class CreateCashTransactionCommand:
    """Command to create and persist a cash transaction.

    This command validates the request, creates the domain entity
    and persists it to the repository.

    Attributes:
        _cash_repo: Repository for cash transaction persistence.
    """

    def __init__(self, cash_repo: CashRepository) -> None:
        """Initialize the command with the cash repository.

        Args:
            cash_repo: Repository for cash transaction persistence.
        """

        self._cash_repo = cash_repo

    async def execute(self, request: CreateCashTransactionRequest) -> CashTransactionResponse:
        """Execute the cash transaction creation flow.

        Steps:
            1. Create the domain entity with business rules applied.
            2. Persist the transaction.
            3. Return the response DTO.

        Args:
            request: Validated cash transaction creation data.

        Returns:
            The created cash transaction as a response DTO.
        """

        logger.info(
            "Creating cash transaction",
            extra={
                "extra_data": {
                    "amount": request.amount,
                    "transaction_type": request.transaction_type.value,
                    "performed_by": str(request.performed_by),
                }
            },
        )

        # Step 1: Create the domain entity
        transaction = CashTransaction.create(
            amount=request.amount,
            transaction_type=request.transaction_type,
            performed_by=request.performed_by,
            description=request.description,
        )

        # Step 2: Persist the transaction
        saved = await self._cash_repo.save(transaction)

        logger.info(
            "Cash transaction created successfully",
            extra={
                "extra_data": {
                    "transaction_id": str(saved.id),
                    "amount": saved.amount,
                }
            },
        )

        # Step 3: Map domain entity to response DTO
        return CashTransactionResponse.model_validate(saved)
