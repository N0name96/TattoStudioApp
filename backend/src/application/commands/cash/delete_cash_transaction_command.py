"""Command to delete a cash transaction in the TattoStudioApp.

This command handles cash transaction deletion:
1. Verify the transaction exists
2. Delete from repository
"""

import logging
from uuid import UUID

from core.errors import EntityNotFoundError
from domain.repositories.cash_repository import CashRepository

logger = logging.getLogger(__name__)


class DeleteCashTransactionCommand:
    """Command to delete a cash transaction from persistence.

    This command verifies the transaction exists before requesting removal.

    Attributes:
        _cash_repo: Repository for cash transaction persistence.
    """

    def __init__(self, cash_repo: CashRepository) -> None:
        """Initialize the command with the cash repository.

        Args:
            cash_repo: Repository for cash transaction persistence.
        """

        self._cash_repo = cash_repo

    async def execute(self, transaction_id: UUID) -> None:
        """Execute the delete cash transaction flow.

        Steps:
            1. Find the transaction by ID.
            2. Delete from repository.

        Args:
            transaction_id: UUID of the transaction to delete.

        Raises:
            EntityNotFoundError: If the transaction does not exist.
        """

        logger.info(
            "Deleting cash transaction",
            extra={"extra_data": {"transaction_id": str(transaction_id)}},
        )

        # Step 1: Find the transaction
        transaction = await self._cash_repo.get_by_id(transaction_id)
        if transaction is None:
            raise EntityNotFoundError(
                f"Cash transaction with id {transaction_id} was not found"
            )

        # Step 2: Delete from repository
        await self._cash_repo.delete(transaction_id)

        logger.info(
            "Cash transaction deleted",
            extra={"extra_data": {"transaction_id": str(transaction_id)}},
        )
