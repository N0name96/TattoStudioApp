"""Command to delete a product."""

import logging
from uuid import UUID
from core.errors import EntityNotFoundError
from domain.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class DeleteProductCommand:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(self, product_id: UUID) -> None:
        product = await self._product_repo.get_by_id(product_id)

        if product is None:
            raise EntityNotFoundError(f"Product {product_id} not found")

        await self._product_repo.delete(product_id)

        logger.info("Product deleted", extra={"extra_data": {"product_id": str(product_id)}})
