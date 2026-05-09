"""Cash transaction domain entity for the TattoStudioApp.

This module contains the CashTransaction entity with all business logic
for cash movement management in the studio's register.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from domain.enums.cash_transaction_type import CashTransactionType


@dataclass
class CashTransaction:
    """Represents a cash transaction in the studio's register.

    This entity tracks all money movements (income and expenses)
    with full audit trail via timestamps.

    Attributes:
        id: Unique identifier for the transaction.
        amount: Transaction amount (always positive).
        transaction_type: Type of transaction (INCOME or EXPENSE).
        description: Optional description of the transaction.
        performed_by: UUID of the user who performed the transaction.
        created_at: When the transaction was created.
        updated_at: When the transaction was last updated.
    """

    id: UUID
    amount: float
    transaction_type: CashTransactionType
    description: str | None
    performed_by: UUID
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        amount: float,
        transaction_type: CashTransactionType,
        performed_by: UUID,
        description: str | None = None,
    ) -> "CashTransaction":
        """Create a new cash transaction.

        This is the factory method for creating cash transactions.
        All transactions start with a fresh UUID and current timestamps.

        Args:
            amount: Transaction amount (must be positive).
            transaction_type: Type of transaction (INCOME or EXPENSE).
            performed_by: UUID of the user performing the transaction.
            description: Optional description of the transaction.

        Returns:
            A new CashTransaction instance.
        """

        now = datetime.now()

        return cls(
            id=uuid4(),
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            performed_by=performed_by,
            created_at=now,
            updated_at=now,
        )

    def update_description(self, description: str) -> None:
        """Update the transaction description.

        Args:
            description: New description for the transaction.
        """

        self.description = description
        self.updated_at = datetime.now()
