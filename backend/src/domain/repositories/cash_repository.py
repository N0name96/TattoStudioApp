"""Cash repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any cash transaction repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/in_memory/cash_repository.py
"""

from datetime import date
from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.cash_transaction_entity import CashTransaction
from domain.enums.cash_transaction_type import CashTransactionType


@runtime_checkable
class CashRepository(Protocol):
    """Interface for CashTransaction persistence.

    This protocol defines the contract that any cash transaction repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer by the in-memory repository.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, transaction_id: UUID) -> CashTransaction | None:
        """Retrieve a cash transaction by its unique identifier.

        Args:
            transaction_id: The UUID of the transaction to find.

        Returns:
            The CashTransaction entity if found, None otherwise.
        """
        ...

    async def save(self, transaction: CashTransaction) -> CashTransaction:
        """Persist a cash transaction entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            transaction: The CashTransaction entity to persist.

        Returns:
            The persisted CashTransaction entity.
        """
        ...

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
        ...

    async def delete(self, transaction_id: UUID) -> None:
        """Remove a cash transaction by its unique identifier.

        Args:
            transaction_id: The UUID of the transaction to delete.
        """
        ...
