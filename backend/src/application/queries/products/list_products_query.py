"""Query to list products."""

from application.dto.responses.products.product_response import ProductResponse
from domain.enums.product_category import ProductCategory
from domain.repositories.product_repository import ProductRepository


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


class ListProductsQuery:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(
        self,
        category: ProductCategory | None = None,
        active_only: bool = True,
    ) -> list[ProductResponse]:
        products = await self._product_repo.list_all(
            category=category, active_only=active_only
        )

        return [_to_response(p) for p in products]

    async def execute_low_stock(self) -> list[ProductResponse]:
        products = await self._product_repo.list_low_stock()

        return [_to_response(p) for p in products]
