"""Tests for product commands."""

from decimal import Decimal
from uuid import uuid4

import pytest

from application.commands.products.create_product_command import CreateProductCommand
from application.dto.requests.products.create_product_request import CreateProductRequest
from domain.enums.product_category import ProductCategory
from infrastructure.persistence.in_memory.product_repository import InMemoryProductRepository


class TestCreateProductCommand:
    @pytest.fixture
    def repo(self):
        return InMemoryProductRepository()

    @pytest.fixture
    def command(self, repo):
        return CreateProductCommand(repo)

    @pytest.mark.asyncio
    async def test_create_product(self, command, repo):
        request = CreateProductRequest(
            name="Test Cream",
            category=ProductCategory.CREAM,
            price=Decimal("15.00"),
            cost_price=Decimal("5.00"),
        )

        response = await command.execute(request)

        assert response.name == "Test Cream"
        assert response.category == ProductCategory.CREAM

        persisted = await repo.get_by_id(response.id)
        assert persisted is not None
