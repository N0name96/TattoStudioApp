"""Command to update product stock."""

import logging
from uuid import UUID
from application.dto.responses.products.product_response import ProductResponse
from core.errors import EntityNotFoundError
from domain.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


def _to_response(product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price.amount,
        cost_price=product.cost_price.amount,
        stock=product.stock,
        min_stock=product.min_stock,
        barcode=product.barcode,
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


class UpdateStockCommand:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def add(self, product_id: UUID, quantity: int) -> ProductResponse:
        product = await self._product_repo.get_by_id(product_id)

        if product is None:
            raise EntityNotFoundError(f"Product {product_id} not found")

        product.add_stock(quantity)

        saved = await self._product_repo.save(product)

        logger.info(
            "Stock added",
            extra={"extra_data": {"product_id": str(product_id), "quantity": quantity, "new_stock": saved.stock}},
        )

        return _to_response(saved)

    async def remove(self, product_id: UUID, quantity: int) -> ProductResponse:
        product = await self._product_repo.get_by_id(product_id)

        if product is None:
            raise EntityNotFoundError(f"Product {product_id} not found")

        product.remove_stock(quantity)

        saved = await self._product_repo.save(product)

        logger.info(
            "Stock removed",
            extra={"extra_data": {"product_id": str(product_id), "quantity": quantity, "new_stock": saved.stock}},
        )

        return _to_response(saved)
