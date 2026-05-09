"""In-memory product repository."""

from uuid import UUID
from domain.entities.product_entity import Product
from domain.enums.product_category import ProductCategory
from domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository:
    def __init__(self) -> None:
        self._storage: dict[UUID, Product] = {}

    async def get_by_id(self, product_id: UUID) -> Product | None:
        return self._storage.get(product_id)

    async def save(self, product: Product) -> Product:
        self._storage[product.id] = product
        return product

    async def list_all(
        self,
        category: ProductCategory | None = None,
        active_only: bool = True,
    ) -> list[Product]:
        products = list(self._storage.values())

        if active_only:
            products = [p for p in products if p.is_active]
        if category is not None:
            products = [p for p in products if p.category == category]

        return products

    async def list_low_stock(self) -> list[Product]:
        return [p for p in self._storage.values() if p.is_active and p.is_low_stock()]

    async def find_by_barcode(self, barcode: str) -> Product | None:
        for product in self._storage.values():
            if product.barcode == barcode:
                return product
        return None

    async def delete(self, product_id: UUID) -> None:
        self._storage.pop(product_id, None)
