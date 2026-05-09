"""Query to get a product by ID."""

from uuid import UUID
from application.dto.responses.products.product_response import ProductResponse
from core.errors import EntityNotFoundError
from domain.repositories.product_repository import ProductRepository


class GetProductQuery:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(self, product_id: UUID) -> ProductResponse:
        product = await self._product_repo.get_by_id(product_id)

        if product is None:
            raise EntityNotFoundError(f"Product {product_id} not found")

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
