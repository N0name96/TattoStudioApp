"""Command to update a product."""

import logging
from uuid import UUID
from domain.value_objects.money_vo import Money
from application.dto.requests.products.update_product_request import UpdateProductRequest
from application.dto.responses.products.product_response import ProductResponse
from core.errors import EntityNotFoundError
from domain.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class UpdateProductCommand:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(
        self, product_id: UUID, request: UpdateProductRequest
    ) -> ProductResponse:
        product = await self._product_repo.get_by_id(product_id)

        if product is None:
            raise EntityNotFoundError(f"Product {product_id} not found")

        kwargs = {}
        if request.name is not None:
            kwargs["name"] = request.name
        if request.description is not None:
            kwargs["description"] = request.description
        if request.category is not None:
            kwargs["category"] = request.category
        if request.price is not None:
            kwargs["price"] = Money(amount=request.price)
        if request.cost_price is not None:
            kwargs["cost_price"] = Money(amount=request.cost_price)
        if request.min_stock is not None:
            kwargs["min_stock"] = request.min_stock
        if request.barcode is not None:
            kwargs["barcode"] = request.barcode

        product.update_details(**kwargs)

        saved = await self._product_repo.save(product)

        return ProductResponse(
            id=saved.id,
            name=saved.name,
            description=saved.description,
            category=saved.category,
            price=saved.price.amount,
            cost_price=saved.cost_price.amount,
            stock=saved.stock,
            min_stock=saved.min_stock,
            barcode=saved.barcode,
            is_active=saved.is_active,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
