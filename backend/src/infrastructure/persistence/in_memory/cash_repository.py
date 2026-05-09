"""In-memory implementation of the CashRepository.

This module provides a non-persistent repository for development
and testing purposes. Data is stored in memory and lost on restart.

Usage:
    from infrastructure.persistence.in_memory.cash_repository import (
        InMemoryCashRepository,
    )
    repo = InMemoryCashRepository()
"""

import logging
from datetime import date
from uuid import UUID

from domain.entities.cash_transaction_entity import CashTransaction
from domain.enums.cash_transaction_type import CashTransactionType

logger = logging.getLogger(__name__)


class InMemoryCashRepository:
    """In-memory implementation of the CashRepository.

    Stores cash transactions in a dictionary for development and testing.
    Data is lost when the application restarts.

    Attributes:
        _storage: Dictionary mapping transaction IDs to entities.
    """

    def __init__(self) -> None:
        """Initialize the in-memory storage."""

        self._storage: dict[UUID, CashTransaction] = {}

        logger.info("InMemoryCashRepository initialized")

    async def get_by_id(self, transaction_id: UUID) -> CashTransaction | None:
        """Retrieve a cash transaction by its unique ID.

        Args:
            transaction_id: The UUID of the transaction to find.

        Returns:
            The CashTransaction entity if found, None otherwise.
        """

        return self._storage.get(transaction_id)

    async def save(self, transaction: CashTransaction) -> CashTransaction:
        """Persist a cash transaction entity (create or update).

        Args:
            transaction: The CashTransaction entity to persist.

        Returns:
            The persisted CashTransaction entity.
        """

        self._storage[transaction.id] = transaction

        logger.debug(
            "CashTransaction saved",
            extra={"extra_data": {"transaction_id": str(transaction.id)}},
        )

        return transaction

    async def list_all(
        self,
        transaction_type: CashTransactionType | None = None,
        performed_by: UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[CashTransaction]:
        """List all cash transactions with optional filters.

        Args:
            transaction_type: Optional filter by transaction type.
            performed_by: Optional filter by user who performed the transaction.
            date_from: Optional filter for transactions on or after this date.
            date_to: Optional filter for transactions on or before this date.

        Returns:
            A list of CashTransaction entities matching the filters.
        """

        results = list(self._storage.values())

        if transaction_type is not None:
            results = [t for t in results if t.transaction_type == transaction_type]

        if performed_by is not None:
            results = [t for t in results if t.performed_by == performed_by]

        if date_from is not None:
            results = [t for t in results if t.created_at.date() >= date_from]

        if date_to is not None:
            results = [t for t in results if t.created_at.date() <= date_to]

        return sorted(results, key=lambda transaction: transaction.created_at, reverse=True)

    async def delete(self, transaction_id: UUID) -> None:
        """Remove a cash transaction by its unique identifier.

        Args:
            transaction_id: The UUID of the transaction to delete.
        """

        self._storage.pop(transaction_id, None)
