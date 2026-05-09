"""Tests for the Money value object.

This module tests the pure business logic of the Money value object,
including validation, arithmetic operations, and immutability.
"""

from decimal import Decimal

import pytest

from domain.value_objects.money_vo import Money


class TestMoneyCreation:
    """Tests for Money creation and validation."""

    def test_create_money_with_positive_amount(self):
        """Test that a Money with a positive amount can be created."""

        money = Money(amount=Decimal("100.00"))

        assert money.amount == Decimal("100.00")
        assert money.currency == "EUR"

    def test_create_money_with_zero_amount(self):
        """Test that a Money with zero amount can be created."""

        money = Money(amount=Decimal("0.00"))

        assert money.amount == Decimal("0.00")

    def test_create_money_with_custom_currency(self):
        """Test that a Money with a custom currency can be created."""

        money = Money(amount=Decimal("50.00"), currency="USD")

        assert money.currency == "USD"
        assert money.amount == Decimal("50.00")

    def test_create_money_with_negative_amount_raises_error(self):
        """Test that creating Money with negative amount raises ValueError."""

        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Money(amount=Decimal("-10.00"))


class TestMoneyAddition:
    """Tests for Money.add() method."""

    def test_add_same_currency(self):
        """Test adding two Money amounts of the same currency."""

        money1 = Money(amount=Decimal("100.00"))
        money2 = Money(amount=Decimal("50.00"))

        result = money1.add(money2)

        assert result.amount == Decimal("150.00")
        assert result.currency == "EUR"

    def test_add_same_currency_usd(self):
        """Test adding two Money amounts in USD."""

        money1 = Money(amount=Decimal("25.50"), currency="USD")
        money2 = Money(amount=Decimal("10.25"), currency="USD")

        result = money1.add(money2)

        assert result.amount == Decimal("35.75")
        assert result.currency == "USD"

    def test_add_different_currencies_raises_error(self):
        """Test that adding Money with different currencies raises ValueError."""

        money1 = Money(amount=Decimal("100.00"), currency="EUR")
        money2 = Money(amount=Decimal("50.00"), currency="USD")

        with pytest.raises(ValueError, match="Cannot add different currencies"):
            money1.add(money2)

    def test_add_does_not_mutate_original(self):
        """Test that add returns a new instance and does not mutate the original."""

        money1 = Money(amount=Decimal("100.00"))
        money2 = Money(amount=Decimal("50.00"))

        result = money1.add(money2)

        assert money1.amount == Decimal("100.00")
        assert result is not money1
        assert result is not money2


class TestMoneySubtraction:
    """Tests for Money.subtract() method."""

    def test_subtract_same_currency(self):
        """Test subtracting two Money amounts of the same currency."""

        money1 = Money(amount=Decimal("100.00"))
        money2 = Money(amount=Decimal("30.00"))

        result = money1.subtract(money2)

        assert result.amount == Decimal("70.00")
        assert result.currency == "EUR"

    def test_subtract_different_currencies_raises_error(self):
        """Test that subtracting Money with different currencies raises ValueError."""

        money1 = Money(amount=Decimal("100.00"), currency="EUR")
        money2 = Money(amount=Decimal("50.00"), currency="USD")

        with pytest.raises(ValueError, match="Cannot subtract different currencies"):
            money1.subtract(money2)

    def test_subtract_does_not_mutate_original(self):
        """Test that subtract returns a new instance and does not mutate the original."""

        money1 = Money(amount=Decimal("100.00"))
        money2 = Money(amount=Decimal("30.00"))

        result = money1.subtract(money2)

        assert money1.amount == Decimal("100.00")


class TestMoneyMultiplication:
    """Tests for Money.multiply() method."""

    def test_multiply_by_integer_factor(self):
        """Test multiplying Money by an integer factor."""

        money = Money(amount=Decimal("50.00"))

        result = money.multiply(Decimal("3"))

        assert result.amount == Decimal("150.00")
        assert result.currency == "EUR"

    def test_multiply_by_fractional_factor(self):
        """Test multiplying Money by a fractional factor (e.g., commission rate)."""

        money = Money(amount=Decimal("100.00"))

        result = money.multiply(Decimal("0.50"))

        assert result.amount == Decimal("50.00")

    def test_multiply_by_zero(self):
        """Test multiplying Money by zero."""

        money = Money(amount=Decimal("100.00"))

        result = money.multiply(Decimal("0"))

        assert result.amount == Decimal("0.00")

    def test_multiply_does_not_mutate_original(self):
        """Test that multiply returns a new instance and does not mutate the original."""

        money = Money(amount=Decimal("50.00"))

        result = money.multiply(Decimal("2"))

        assert money.amount == Decimal("50.00")
        assert result is not money


class TestMoneyString:
    """Tests for Money.__str__() method."""

    def test_string_representation(self):
        """Test that __str__ returns a human-readable format."""

        money = Money(amount=Decimal("50.00"))

        assert str(money) == "50.00 EUR"

    def test_string_representation_usd(self):
        """Test string representation for USD."""

        money = Money(amount=Decimal("25.99"), currency="USD")

        assert str(money) == "25.99 USD"


class TestMoneyImmutability:
    """Tests for Money immutability (frozen dataclass)."""

    def test_money_is_immutable(self):
        """Test that Money cannot be modified after creation."""

        money = Money(amount=Decimal("100.00"))

        with pytest.raises(Exception):
            money.amount = Decimal("200.00")

    def test_money_currency_is_immutable(self):
        """Test that Money currency cannot be modified."""

        money = Money(amount=Decimal("100.00"))

        with pytest.raises(Exception):
            money.currency = "USD"
