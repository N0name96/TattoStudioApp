"""DateRange value object for the TattoStudioApp.

Represents a date range with start and end dates as an immutable value object.
Provides utility methods for range containment and overlap checks.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    """Value object representing a range of dates.

    Immutable by design. The start_date must be on or before the end_date.
    Provides methods for checking containment and overlap with other ranges.

    Attributes:
        start_date: The inclusive start date of the range.
        end_date: The inclusive end date of the range.
    """

    start_date: date
    end_date: date


    def __post_init__(self) -> None:
        """Validate that start_date is not after end_date.

        Raises:
            ValueError: If start_date is after end_date.
        """

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) must be on or before end_date ({self.end_date})"
            )


    def contains(self, target_date: date) -> bool:
        """Check if a date falls within this range (inclusive).

        Args:
            target_date: The date to check.

        Returns:
            True if the date is within the range, False otherwise.
        """

        return self.start_date <= target_date <= self.end_date


    def overlaps(self, other: "DateRange") -> bool:
        """Check if this range overlaps with another DateRange.

        Two ranges overlap if they share at least one date.

        Args:
            other: Another DateRange to check overlap with.

        Returns:
            True if the ranges overlap, False otherwise.
        """

        return self.start_date <= other.end_date and other.start_date <= self.end_date


    def duration_days(self) -> int:
        """Calculate the number of days in the range (inclusive).

        Returns:
            The number of days from start_date to end_date inclusive.
        """

        delta = self.end_date - self.start_date

        return delta.days + 1
