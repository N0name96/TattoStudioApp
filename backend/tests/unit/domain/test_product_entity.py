"""Tests for the Product domain entity."""

from decimal import Decimal
from uuid import uuid4

import pytest

from core.errors import BusinessRuleError
from domain.entities.product_entity import Product
from domain.enums.product_category import ProductCategory
from domain.value_objects.money_vo import Money


class TestProductCreation:
    def test_create_product_with_valid_data(self):
        product = Product.create(
            name="Tattoo Cream",
            category=ProductCategory.CREAM,
            price=Money(amount=Decimal("15.00")),
            cost_price=Money(amount=Decimal("5.00")),
        )

        assert product.name == "Tattoo Cream"
        assert product.category == ProductCategory.CREAM
        assert product.price.amount == Decimal("15.00")
        assert product.cost_price.amount == Decimal("5.00")
        assert product.stock == 0
        assert product.min_stock == 5
        assert product.is_active is True
        assert product.barcode is None

    def test_create_product_with_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Product.create(
                name="Bad",
                category=ProductCategory.INK,
                price=Money(amount=Decimal("-5.00")),
                cost_price=Money(amount=Decimal("1.00")),
            )

    def test_create_product_with_negative_stock_raises_error(self):
        with pytest.raises(BusinessRuleError, match="Stock cannot be negative"):
            Product.create(
                name="Bad",
                category=ProductCategory.INK,
                price=Money(amount=Decimal("10.00")),
                cost_price=Money(amount=Decimal("2.00")),
                stock=-5,
            )

    def test_profit_margin(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.JEWELRY,
            price=Money(amount=Decimal("30.00")),
            cost_price=Money(amount=Decimal("10.00")),
        )

        assert product.profit_margin() == Decimal("2.0")

    def test_is_low_stock(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.MERCHANDISE,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
            stock=3,
            min_stock=5,
        )

        assert product.is_low_stock() is True


class TestStockOperations:
    def test_add_stock(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
            stock=10,
        )

        product.add_stock(5)

        assert product.stock == 15

    def test_remove_stock(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
            stock=10,
        )

        product.remove_stock(3)

        assert product.stock == 7

    def test_remove_stock_insufficient_raises_error(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
            stock=5,
        )

        with pytest.raises(BusinessRuleError, match="Insufficient stock"):
            product.remove_stock(10)

    def test_add_stock_negative_raises_error(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
        )

        with pytest.raises(BusinessRuleError, match="must be positive"):
            product.add_stock(0)


class TestProductActivation:
    def test_deactivate(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
        )

        product.deactivate()

        assert product.is_active is False

    def test_activate(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
        )

        product.deactivate()
        product.activate()

        assert product.is_active is True

    def test_deactivate_twice_raises_error(self):
        product = Product.create(
            name="Test",
            category=ProductCategory.INK,
            price=Money(amount=Decimal("10.00")),
            cost_price=Money(amount=Decimal("2.00")),
        )

        product.deactivate()

        with pytest.raises(BusinessRuleError, match="already inactive"):
            product.deactivate()
