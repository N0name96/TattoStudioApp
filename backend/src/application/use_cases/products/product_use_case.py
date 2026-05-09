"""Use case for product operations."""

from uuid import UUID
from application.commands.products.create_product_command import CreateProductCommand
from application.commands.products.delete_product_command import DeleteProductCommand
from application.commands.products.update_product_command import UpdateProductCommand
from application.commands.products.update_stock_command import UpdateStockCommand
from application.dto.requests.products.create_product_request import CreateProductRequest
from application.dto.requests.products.update_product_request import UpdateProductRequest
from application.dto.responses.products.product_response import ProductResponse
from application.queries.products.get_product_query import GetProductQuery
from application.queries.products.list_products_query import ListProductsQuery
from domain.enums.product_category import ProductCategory
from domain.repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo
        self._create_command = CreateProductCommand(product_repo)
        self._update_command = UpdateProductCommand(product_repo)
        self._stock_command = UpdateStockCommand(product_repo)
        self._delete_command = DeleteProductCommand(product_repo)
        self._get_query = GetProductQuery(product_repo)
        self._list_query = ListProductsQuery(product_repo)

    async def create_product(self, request: CreateProductRequest) -> ProductResponse:
        return await self._create_command.execute(request)

    async def get_product(self, product_id: UUID) -> ProductResponse:
        return await self._get_query.execute(product_id)

    async def list_products(
        self,
        category: ProductCategory | None = None,
        active_only: bool = True,
    ) -> list[ProductResponse]:
        return await self._list_query.execute(category=category, active_only=active_only)

    async def list_low_stock(self) -> list[ProductResponse]:
        return await self._list_query.execute_low_stock()

    async def update_product(
        self, product_id: UUID, request: UpdateProductRequest
    ) -> ProductResponse:
        return await self._update_command.execute(product_id, request)

    async def add_stock(self, product_id: UUID, quantity: int) -> ProductResponse:
        return await self._stock_command.add(product_id, quantity)

    async def remove_stock(self, product_id: UUID, quantity: int) -> ProductResponse:
        return await self._stock_command.remove(product_id, quantity)

    async def delete_product(self, product_id: UUID) -> None:
        await self._delete_command.execute(product_id)
