"""Product domain entity for the TattoStudioApp.

This module contains the Product entity with all business logic
for product management including stock operations and price validation.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.product_category import ProductCategory
from domain.value_objects.money_vo import Money


@dataclass
class Product:
    id: UUID
    name: str
    description: str | None
    category: ProductCategory
    price: Money
    cost_price: Money
    stock: int
    min_stock: int
    barcode: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


    @classmethod
    def create(
        cls,
        name: str,
        category: ProductCategory,
        price: Money,
        cost_price: Money,
        stock: int = 0,
        min_stock: int = 5,
        description: str | None = None,
        barcode: str | None = None,
    ) -> "Product":
        if price.amount <= 0:
            raise BusinessRuleError("Price must be greater than zero")

        if cost_price.amount < 0:
            raise BusinessRuleError("Cost price cannot be negative")

        if stock < 0:
            raise BusinessRuleError("Stock cannot be negative")

        if min_stock < 0:
            raise BusinessRuleError("Minimum stock cannot be negative")

        now = datetime.now()

        return cls(
            id=uuid4(),
            name=name,
            description=description,
            category=category,
            price=price,
            cost_price=cost_price,
            stock=stock,
            min_stock=min_stock,
            barcode=barcode,
            is_active=True,
            created_at=now,
            updated_at=now,
        )


    def add_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise BusinessRuleError("Stock quantity must be positive")

        if not self.is_active:
            raise BusinessRuleError("Cannot add stock to an inactive product")

        self.stock += quantity
        self.updated_at = datetime.now()


    def remove_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise BusinessRuleError("Stock quantity must be positive")

        if not self.is_active:
            raise BusinessRuleError("Cannot remove stock from an inactive product")

        if self.stock < quantity:
            raise BusinessRuleError(
                f"Insufficient stock: have {self.stock}, need {quantity}"
            )

        self.stock -= quantity
        self.updated_at = datetime.now()


    def update_details(
        self,
        name: str | None = None,
        description: str | None = None,
        category: ProductCategory | None = None,
        price: Money | None = None,
        cost_price: Money | None = None,
        min_stock: int | None = None,
        barcode: str | None = None,
    ) -> None:
        if price is not None and price.amount <= 0:
            raise BusinessRuleError("Price must be greater than zero")

        if cost_price is not None and cost_price.amount < 0:
            raise BusinessRuleError("Cost price cannot be negative")

        if min_stock is not None and min_stock < 0:
            raise BusinessRuleError("Minimum stock cannot be negative")

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if category is not None:
            self.category = category
        if price is not None:
            self.price = price
        if cost_price is not None:
            self.cost_price = cost_price
        if min_stock is not None:
            self.min_stock = min_stock
        if barcode is not None:
            self.barcode = barcode

        self.updated_at = datetime.now()


    def deactivate(self) -> None:
        if not self.is_active:
            raise BusinessRuleError("Product is already inactive")

        self.is_active = False
        self.updated_at = datetime.now()


    def activate(self) -> None:
        if self.is_active:
            raise BusinessRuleError("Product is already active")

        self.is_active = True
        self.updated_at = datetime.now()


    def is_low_stock(self) -> bool:
        return self.stock <= self.min_stock


    def profit_margin(self) -> Decimal:
        if self.cost_price.amount == 0:
            return Decimal("0")

        return (self.price.amount - self.cost_price.amount) / self.cost_price.amount
