"""Query to retrieve a cash transaction by id in the TattoStudioApp.

This module provides the query for fetching a single cash transaction
by its unique identifier.
"""

import logging
from uuid import UUID

from application.dto.responses.cash.cash_transaction_response import CashTransactionResponse
from core.errors import EntityNotFoundError
from domain.repositories.cash_repository import CashRepository

logger = logging.getLogger(__name__)


class GetCashTransactionQuery:
    """Query to fetch a cash transaction by unique identifier.

    This query retrieves a single cash transaction and maps it
    to the response DTO.

    Attributes:
        _cash_repo: Repository for cash transaction persistence.
    """

    def __init__(self, cash_repo: CashRepository) -> None:
        """Initialize the query with the cash repository.

        Args:
            cash_repo: Repository for cash transaction persistence.
        """

        self._cash_repo = cash_repo

    async def execute(self, transaction_id: UUID) -> CashTransactionResponse:
        """Execute the get cash transaction query.

        Retrieves a single cash transaction and maps it to the response DTO.

        Args:
            transaction_id: UUID of the transaction to retrieve.

        Returns:
            The cash transaction as a response DTO.

        Raises:
            EntityNotFoundError: If the transaction does not exist.
        """

        logger.debug(
            "Fetching cash transaction",
            extra={"extra_data": {"transaction_id": str(transaction_id)}},
        )

        # Step 1: Find the transaction
        transaction = await self._cash_repo.get_by_id(transaction_id)
        if transaction is None:
            raise EntityNotFoundError(
                f"Cash transaction with id {transaction_id} was not found"
            )

        # Step 2: Map domain entity to response DTO
        return CashTransactionResponse.model_validate(transaction)
