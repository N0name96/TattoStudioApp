"""Money value object for the TattoStudioApp.

Represents a monetary amount with its currency as an immutable value object.
All arithmetic operations return new Money instances.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """Value object representing a monetary amount with currency.

    Immutable by design. All operations return new instances
    to prevent accidental mutation of financial data.

    Attributes:
        amount: The monetary amount as a Decimal.
        currency: ISO 4217 currency code, defaults to "EUR".
    """

    amount: Decimal
    currency: str = "EUR"


    def __post_init__(self) -> None:
        """Validate that the amount is not negative.

        Raises:
            ValueError: If the amount is negative.
        """

        if self.amount < 0:
            raise ValueError("Amount cannot be negative")


    def add(self, other: "Money") -> "Money":
        """Add two Money amounts of the same currency.

        Args:
            other: Another Money instance to add.

        Returns:
            A new Money instance with the summed amount.

        Raises:
            ValueError: If the currencies do not match.
        """

        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add different currencies: {self.currency} and {other.currency}"
            )

        return Money(amount=self.amount + other.amount, currency=self.currency)


    def subtract(self, other: "Money") -> "Money":
        """Subtract another Money amount from this one.

        Args:
            other: Another Money instance to subtract.

        Returns:
            A new Money instance with the difference.

        Raises:
            ValueError: If the currencies do not match.
        """

        if self.currency != other.currency:
            raise ValueError(
                f"Cannot subtract different currencies: {self.currency} and {other.currency}"
            )

        return Money(amount=self.amount - other.amount, currency=self.currency)


    def multiply(self, factor: Decimal) -> "Money":
        """Multiply the amount by a scalar factor.

        Args:
            factor: The scalar factor to multiply by.

        Returns:
            A new Money instance with the multiplied amount.
        """

        return Money(amount=self.amount * factor, currency=self.currency)


    def __str__(self) -> str:
        """Format the Money as a human-readable string.

        Returns:
            A string like '50.00 EUR'.
        """

        return f"{self.amount} {self.currency}"
