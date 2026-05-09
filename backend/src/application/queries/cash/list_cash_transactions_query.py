"""Query to list cash transactions with optional filters in the TattoStudioApp.

This module provides the query for listing cash transactions
with optional filtering by type, performer, and date range.
"""

import logging
from datetime import date
from uuid import UUID

from application.dto.responses.cash.cash_transaction_response import CashTransactionResponse
from domain.enums.cash_transaction_type import CashTransactionType
from domain.repositories.cash_repository import CashRepository

logger = logging.getLogger(__name__)


class ListCashTransactionsQuery:
    """Query to list cash transactions with optional filtering.

    This query retrieves all cash transactions matching the provided
    filters and maps them to response DTOs.

    Attributes:
        _cash_repo: Repository for cash transaction persistence.
    """

    def __init__(self, cash_repo: CashRepository) -> None:
        """Initialize the query with the cash repository.

        Args:
            cash_repo: Repository for cash transaction persistence.
        """

        self._cash_repo = cash_repo

    async def execute(
        self,
        transaction_type: CashTransactionType | None = None,
        performed_by: UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[CashTransactionResponse]:
        """Execute the list cash transactions query.

        Returns transactions filtered by type, performer, and date range.

        Args:
            transaction_type: Optional filter by transaction type.
            performed_by: Optional filter by user who performed the transaction.
            date_from: Optional filter for transactions on or after this date.
            date_to: Optional filter for transactions on or before this date.

        Returns:
            A list of cash transaction response DTOs.
        """

        logger.debug(
            "Listing cash transactions",
            extra={
                "extra_data": {
                    "transaction_type": transaction_type.value if transaction_type else None,
                    "performed_by": str(performed_by) if performed_by else None,
                    "date_from": date_from,
                    "date_to": date_to,
                }
            },
        )

        # Step 1: Fetch transactions from repository with filters
        transactions = await self._cash_repo.list_all(
            transaction_type=transaction_type,
            performed_by=performed_by,
            date_from=date_from,
            date_to=date_to,
        )

        # Step 2: Map domain entities to response DTOs
        return [CashTransactionResponse.model_validate(tx) for tx in transactions]
