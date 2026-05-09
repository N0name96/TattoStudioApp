"""Cash transaction type enumeration for the TattoStudioApp.

This module defines the possible types of cash movements
in the studio's register.
"""

from enum import Enum


class CashTransactionType(str, Enum):
    """Possible transaction types for cash movements.

    Uses str mixin for easy JSON serialization.

    Attributes:
        INCOME: Money coming into the studio (e.g., client payments).
        EXPENSE: Money going out of the studio (e.g., supplies, rent).
    """

    INCOME = "income"
    EXPENSE = "expense"
