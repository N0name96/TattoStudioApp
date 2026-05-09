"""Commission calculator domain service for the TattoStudioApp.

Calculates artist commissions for services performed at the studio.
The commission rate is configurable per service type and can be
customized per artist.

This is a pure domain service with no external dependencies,
making it easily testable in isolation.
"""

from decimal import Decimal
from typing import ClassVar

from domain.enums.service_type import ServiceType
from domain.value_objects.money_vo import Money


class CommissionCalculator:
    """Calculates artist commissions based on service type rates.

    The calculator uses a configurable percentage rate per service type.
    Default rates are provided for each service type and can be overridden
    per artist or per use case.

    All calculations return Money value objects to ensure
    currency consistency and immutability.

    Attributes:
        DEFAULT_RATES: Default commission rates per service type (as Decimal percentage).
        _rates: The current commission rates used for calculations.
    """

    DEFAULT_RATES: ClassVar[dict[ServiceType, Decimal]] = {
        ServiceType.TATTOO: Decimal("0.50"),
        ServiceType.PIERCING: Decimal("0.40"),
        ServiceType.MICROPIGMENTATION: Decimal("0.45"),
        ServiceType.LASER: Decimal("0.45"),
        ServiceType.DENTAL_GEMS: Decimal("0.40"),
    }


    def __init__(self, rates: dict[ServiceType, Decimal] | None = None) -> None:
        """Initialize the calculator with optional custom rates.

        Args:
            rates: Custom commission rates to override defaults.
                   Only provided rates are overridden; missing ones use defaults.
        """

        self._rates = dict(self.DEFAULT_RATES)

        if rates is not None:
            for service_type, rate in rates.items():
                self._validate_rate(service_type, rate)

            self._rates.update(rates)


    def calculate_commission(
        self,
        service_price: Money,
        service_type: ServiceType,
    ) -> Money:
        """Calculate the commission for a single service.

        Args:
            service_price: The total price of the service.
            service_type: The type of service performed.

        Returns:
            A Money instance representing the commission amount.

        Raises:
            ValueError: If the service_type has no configured rate.
        """

        rate = self.get_rate(service_type)

        return service_price.multiply(rate)


    def calculate_total_commissions(
        self,
        services: list[tuple[Money, ServiceType]],
    ) -> Money:
        """Calculate the total commission for multiple services.

        Args:
            services: A list of (price, service_type) tuples.

        Returns:
            A Money instance representing the total commission across all services.
        """

        total = Money(amount=Decimal("0"))

        for price, service_type in services:
            commission = self.calculate_commission(price, service_type)
            total = total.add(commission)

        return total


    def get_rate(self, service_type: ServiceType) -> Decimal:
        """Get the current commission rate for a service type.

        Args:
            service_type: The service type to look up.

        Returns:
            The commission rate as a Decimal (e.g., 0.50 for 50%).

        Raises:
            ValueError: If the service type has no configured rate.
        """

        rate = self._rates.get(service_type)

        if rate is None:
            raise ValueError(f"No commission rate configured for {service_type}")

        return rate


    def set_rate(self, service_type: ServiceType, rate: Decimal) -> None:
        """Update the commission rate for a service type.

        Args:
            service_type: The service type to update.
            rate: The new commission rate (0.0 to 1.0).

        Raises:
            ValueError: If the rate is not between 0.0 and 1.0.
        """

        self._validate_rate(service_type, rate)

        self._rates[service_type] = rate


    def _validate_rate(self, service_type: ServiceType, rate: Decimal) -> None:
        """Validate that a commission rate is within the valid range.

        Args:
            service_type: The service type for the error message context.
            rate: The commission rate to validate.

        Raises:
            ValueError: If the rate is less than 0 or greater than 1.
        """

        if rate < 0 or rate > 1:
            raise ValueError(
                f"Commission rate for {service_type} must be between 0 and 1, got {rate}"
            )
