"""Use case for cash transaction operations in the TattoStudioApp.

This module provides a high-level interface for cash transaction operations,
orchestrating commands and queries. It acts as the entry point for
the API layer to interact with the cash domain.
"""

from datetime import date
from uuid import UUID

from application.commands.cash.create_cash_transaction_command import (
    CreateCashTransactionCommand,
)
from application.commands.cash.delete_cash_transaction_command import (
    DeleteCashTransactionCommand,
)
from application.dto.requests.cash.create_cash_transaction_request import (
    CreateCashTransactionRequest,
)
from application.dto.responses.cash.cash_transaction_response import (
    CashTransactionResponse,
)
from application.queries.cash.get_cash_transaction_query import GetCashTransactionQuery
from application.queries.cash.list_cash_transactions_query import (
    ListCashTransactionsQuery,
)
from domain.enums.cash_transaction_type import CashTransactionType
from domain.repositories.cash_repository import CashRepository


class CashUseCase:
    """Use case for cash transaction operations.

    Orchestrates commands and queries for the cash module.
    Provides a single entry point for the API layer.

    Attributes:
        _cash_repo: Repository for cash transaction persistence.
        _create_command: Command for creating transactions.
        _get_query: Query for retrieving a single transaction.
        _list_query: Query for listing transactions.
        _delete_command: Command for deleting transactions.
    """

    def __init__(self, cash_repo: CashRepository) -> None:
        """Initialize the use case with the cash repository.

        Args:
            cash_repo: Repository for cash transaction persistence.
        """

        self._cash_repo = cash_repo
        self._create_command = CreateCashTransactionCommand(cash_repo)
        self._get_query = GetCashTransactionQuery(cash_repo)
        self._list_query = ListCashTransactionsQuery(cash_repo)
        self._delete_command = DeleteCashTransactionCommand(cash_repo)

    async def create_transaction(
        self, request: CreateCashTransactionRequest
    ) -> CashTransactionResponse:
        """Create a new cash transaction.

        Args:
            request: Validated cash transaction creation data.

        Returns:
            The created cash transaction as a response DTO.
        """

        return await self._create_command.execute(request)

    async def get_transaction(self, transaction_id: UUID) -> CashTransactionResponse:
        """Retrieve a single cash transaction by its identifier.

        Args:
            transaction_id: UUID of the transaction to retrieve.

        Returns:
            The cash transaction as a response DTO.
        """

        return await self._get_query.execute(transaction_id)

    async def list_transactions(
        self,
        transaction_type: CashTransactionType | None = None,
        performed_by: UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[CashTransactionResponse]:
        """List cash transactions with optional filters.

        Args:
            transaction_type: Optional filter by transaction type.
            performed_by: Optional filter by user who performed the transaction.
            date_from: Optional filter for transactions on or after this date.
            date_to: Optional filter for transactions on or before this date.

        Returns:
            A list of cash transaction response DTOs.
        """

        return await self._list_query.execute(
            transaction_type=transaction_type,
            performed_by=performed_by,
            date_from=date_from,
            date_to=date_to,
        )

    async def delete_transaction(self, transaction_id: UUID) -> None:
        """Delete a cash transaction by its identifier.

        Args:
            transaction_id: UUID of the transaction to delete.
        """

        await self._delete_command.execute(transaction_id)
