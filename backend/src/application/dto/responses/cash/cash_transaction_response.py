"""Response DTOs for the cash module.

Contains Pydantic models for serializing cash transaction data.
These DTOs are used by the API layer to format responses.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CashTransactionResponse(BaseModel):
    """Response DTO for cash transaction data.

    Used to return cash transaction information to the API client.
    Maps from domain entity to a serializable format.

    Attributes:
        id: Unique identifier for the transaction.
        amount: Transaction amount.
        transaction_type: Type of transaction (INCOME or EXPENSE).
        performed_by: UUID of the user who performed the transaction.
        description: Optional description of the transaction.
        created_at: When the transaction was created.
        updated_at: When the transaction was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: float
    transaction_type: str
    performed_by: UUID
    description: str | None
    created_at: datetime
    updated_at: datetime
