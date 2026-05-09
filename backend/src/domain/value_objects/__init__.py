"""Domain value objects for the TattoStudioApp.

Value objects are immutable, self-validating objects that represent
domain concepts without identity. They are defined with @dataclass(frozen=True)
to ensure immutability and value equality.
"""

from domain.value_objects.date_range_vo import DateRange
from domain.value_objects.email_vo import Email
from domain.value_objects.money_vo import Money

__all__ = ["DateRange", "Email", "Money"]
