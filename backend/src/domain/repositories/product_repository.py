"""Product repository interface (Protocol) for the TattoStudioApp."""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.product_entity import Product
from domain.enums.product_category import ProductCategory


@runtime_checkable
class ProductRepository(Protocol):
    async def get_by_id(self, product_id: UUID) -> Product | None: ...
    async def save(self, product: Product) -> Product: ...
    async def list_all(
        self,
        category: ProductCategory | None = None,
        active_only: bool = True,
    ) -> list[Product]: ...
    async def list_low_stock(self) -> list[Product]: ...
    async def find_by_barcode(self, barcode: str) -> Product | None: ...
    async def delete(self, product_id: UUID) -> None: ...
