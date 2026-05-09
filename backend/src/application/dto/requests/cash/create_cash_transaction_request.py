"""Request DTOs for the cash module.

Contains Pydantic models for validating incoming cash transaction data.
These DTOs are used by the API layer and commands to validate input.
"""

from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.cash_transaction_type import CashTransactionType


class CreateCashTransactionRequest(BaseModel):
    """Request DTO for creating a new cash transaction.

    Contains all the data needed to record a cash movement
    in the studio's register.

    Attributes:
        amount: Transaction amount (must be positive).
        transaction_type: Type of transaction (INCOME or EXPENSE).
        performed_by: UUID of the user performing the transaction.
        description: Optional description of the transaction.
    """

    amount: float = Field(gt=0)
    transaction_type: CashTransactionType
    performed_by: UUID
    description: str | None = Field(default=None, max_length=500)
