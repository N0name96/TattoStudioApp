"""Tests for the CommissionCalculator domain service.

This module tests the commission calculation logic for artist services,
including default rates, custom rates, single and multiple service calculations,
and rate validation.

No mocks are needed since CommissionCalculator is a pure domain service.
"""

from decimal import Decimal

import pytest

from domain.enums.service_type import ServiceType
from domain.services.commission_calculator import CommissionCalculator
from domain.value_objects.money_vo import Money


class TestDefaultRates:
    """Tests for default commission rates."""

    def test_all_service_types_have_default_rates(self):
        """Test that every ServiceType has a default rate."""

        calculator = CommissionCalculator()

        for service_type in ServiceType:
            rate = calculator.get_rate(service_type)

            assert isinstance(rate, Decimal)
            assert 0 < rate <= 1

    def test_tattoo_default_rate(self):
        """Test the default rate for TATTOO."""

        calculator = CommissionCalculator()

        rate = calculator.get_rate(ServiceType.TATTOO)

        assert rate == Decimal("0.50")

    def test_piercing_default_rate(self):
        """Test the default rate for PIERCING."""

        calculator = CommissionCalculator()

        rate = calculator.get_rate(ServiceType.PIERCING)

        assert rate == Decimal("0.40")


class TestSingleCommissionCalculation:
    """Tests for calculate_commission() for a single service."""

    def test_calculate_tattoo_commission(self):
        """Test commission calculation for a tattoo service."""

        calculator = CommissionCalculator()
        price = Money(amount=Decimal("200.00"))

        commission = calculator.calculate_commission(price, ServiceType.TATTOO)

        assert commission.amount == Decimal("100.00")
        assert commission.currency == "EUR"

    def test_calculate_piercing_commission(self):
        """Test commission calculation for a piercing service."""

        calculator = CommissionCalculator()
        price = Money(amount=Decimal("50.00"))

        commission = calculator.calculate_commission(price, ServiceType.PIERCING)

        assert commission.amount == Decimal("20.00")

    def test_calculate_free_service_commission(self):
        """Test that a free service yields zero commission."""

        calculator = CommissionCalculator()
        price = Money(amount=Decimal("0.00"))

        commission = calculator.calculate_commission(price, ServiceType.TATTOO)

        assert commission.amount == Decimal("0.00")

    def test_calculate_with_fractional_price(self):
        """Test commission with a price that has cents."""

        calculator = CommissionCalculator()
        price = Money(amount=Decimal("99.99"))

        commission = calculator.calculate_commission(price, ServiceType.TATTOO)

        assert commission.amount == Decimal("49.995")


class TestMultipleCommissionCalculation:
    """Tests for calculate_total_commissions() for multiple services."""

    def test_calculate_total_for_multiple_services(self):
        """Test total commission across multiple services."""

        calculator = CommissionCalculator()
        services = [
            (Money(amount=Decimal("200.00")), ServiceType.TATTOO),
            (Money(amount=Decimal("50.00")), ServiceType.PIERCING),
        ]

        total = calculator.calculate_total_commissions(services)

        # Tattoo: 200 * 0.50 = 100, Piercing: 50 * 0.40 = 20, Total = 120
        assert total.amount == Decimal("120.00")

    def test_calculate_total_for_empty_list(self):
        """Test that an empty list returns zero."""

        calculator = CommissionCalculator()

        total = calculator.calculate_total_commissions([])

        assert total.amount == Decimal("0.00")

    def test_calculate_total_preserves_currency(self):
        """Test that total commission preserves the currency."""

        calculator = CommissionCalculator()
        services = [
            (Money(amount=Decimal("100.00")), ServiceType.TATTOO),
        ]

        total = calculator.calculate_total_commissions(services)

        assert total.currency == "EUR"

    def test_calculate_total_with_three_different_services(self):
        """Test total commission with three different service types."""

        calculator = CommissionCalculator()
        services = [
            (Money(amount=Decimal("300.00")), ServiceType.TATTOO),       # 300*0.50 = 150
            (Money(amount=Decimal("80.00")), ServiceType.PIERCING),      # 80*0.40 = 32
            (Money(amount=Decimal("150.00")), ServiceType.LASER),        # 150*0.45 = 67.5
        ]

        total = calculator.calculate_total_commissions(services)

        assert total.amount == Decimal("249.50")


class TestCustomRates:
    """Tests for custom commission rates."""

    def test_custom_rates_override_defaults(self):
        """Test that custom rates replace default rates."""

        custom_rates = {ServiceType.TATTOO: Decimal("0.60")}
        calculator = CommissionCalculator(rates=custom_rates)
        price = Money(amount=Decimal("200.00"))

        commission = calculator.calculate_commission(price, ServiceType.TATTOO)

        assert commission.amount == Decimal("120.00")

    def test_custom_rates_partial_override(self):
        """Test that only specified rates are overridden."""

        custom_rates = {ServiceType.TATTOO: Decimal("0.60")}
        calculator = CommissionCalculator(rates=custom_rates)

        # TATTOO should use custom rate
        assert calculator.get_rate(ServiceType.TATTOO) == Decimal("0.60")

        # PIERCING should still use default
        assert calculator.get_rate(ServiceType.PIERCING) == Decimal("0.40")


class TestRateManagement:
    """Tests for get_rate() and set_rate() methods."""

    def test_set_rate_with_valid_value(self):
        """Test setting a rate with a valid value (0.0 to 1.0)."""

        calculator = CommissionCalculator()

        calculator.set_rate(ServiceType.TATTOO, Decimal("0.70"))

        assert calculator.get_rate(ServiceType.TATTOO) == Decimal("0.70")

    def test_set_rate_with_zero(self):
        """Test setting a rate to zero."""

        calculator = CommissionCalculator()

        calculator.set_rate(ServiceType.TATTOO, Decimal("0.0"))

        assert calculator.get_rate(ServiceType.TATTOO) == Decimal("0.0")

    def test_set_rate_with_one(self):
        """Test setting a rate to 1.0 (100%)."""

        calculator = CommissionCalculator()

        calculator.set_rate(ServiceType.TATTOO, Decimal("1.0"))

        assert calculator.get_rate(ServiceType.TATTOO) == Decimal("1.0")

    def test_set_rate_with_negative_value_raises_error(self):
        """Test that setting a negative rate raises ValueError."""

        calculator = CommissionCalculator()

        with pytest.raises(
            ValueError, match="must be between 0 and 1"
        ):
            calculator.set_rate(ServiceType.TATTOO, Decimal("-0.10"))

    def test_set_rate_above_one_raises_error(self):
        """Test that setting a rate above 1.0 raises ValueError."""

        calculator = CommissionCalculator()

        with pytest.raises(
            ValueError, match="must be between 0 and 1"
        ):
            calculator.set_rate(ServiceType.TATTOO, Decimal("1.50"))

    def test_custom_rates_with_invalid_value_raises_error(self):
        """Test that invalid custom rates at init raise ValueError."""

        custom_rates = {ServiceType.TATTOO: Decimal("-0.10")}

        with pytest.raises(
            ValueError, match="must be between 0 and 1"
        ):
            CommissionCalculator(rates=custom_rates)

    def test_get_rate_for_unconfigured_service_type_raises_error(self):
        """Test that getting rate for an unlisted service type raises ValueError.

        Note: This would only happen if a ServiceType is added without
        a corresponding default rate or custom rate.
        """

        calculator = CommissionCalculator()

        # Delete the rate to simulate an unconfigured type
        calculator._rates.pop(ServiceType.TATTOO)

        with pytest.raises(ValueError, match="No commission rate configured"):
            calculator.get_rate(ServiceType.TATTOO)
