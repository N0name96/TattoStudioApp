"""Email value object for the TattoStudioApp.

Represents a validated email address as an immutable value object.
Ensures email format correctness at the domain level.
"""

import re
from dataclasses import dataclass


# Regex pattern for basic email format validation
_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@dataclass(frozen=True)
class Email:
    """Value object representing a validated email address.

    Immutable by design. The email format is validated on creation
    and cannot be changed afterwards.

    Attributes:
        value: The email address string.
    """

    value: str


    def __post_init__(self) -> None:
        """Validate the email format.

        Raises:
            ValueError: If the email format is invalid.
        """

        if not _EMAIL_PATTERN.match(self.value):
            raise ValueError(f"Invalid email format: {self.value}")


    def __str__(self) -> str:
        """Return the email address as a string.

        Returns:
            The email address value.
        """

        return self.value
