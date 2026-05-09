"""Supabase implementation of the ProductRepository."""

import logging
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.product_entity import Product
from domain.enums.product_category import ProductCategory
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import map_to_product, map_to_product_dict

logger = logging.getLogger(__name__)

TABLE = "products"


class SupabaseProductRepository:
    TABLE = TABLE

    async def get_by_id(self, product_id: UUID) -> Product | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("id", str(product_id)).execute()
            if not response.data:
                return None
            return map_to_product(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get product: {e}")

    async def save(self, product: Product) -> Product:
        try:
            client = await SupabaseClientSingleton.get_client()
            data = map_to_product_dict(product)
            response = client.table(self.TABLE).upsert(data).execute()
            if not response.data:
                raise DatabaseError("Failed to save product: no data returned")
            return map_to_product(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save product: {e}")

    async def list_all(
        self,
        category: ProductCategory | None = None,
        active_only: bool = True,
    ) -> list[Product]:
        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*").order("name")
            if active_only:
                query = query.eq("is_active", True)
            if category is not None:
                query = query.eq("category", category.value)
            response = query.execute()
            return [map_to_product(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list products: {e}")

    async def list_low_stock(self) -> list[Product]:
        try:
            client = await SupabaseClientSingleton.get_client()
            # Products where stock <= min_stock and active
            response = (
                client.table(self.TABLE)
                .select("*")
                .eq("is_active", True)
                .lte("stock", client.table(self.TABLE).select("min_stock"))
                .execute()
            )
            # Supabase doesn't support self-referencing in a single query easily,
            # so we fetch all active and filter in memory for low stock
            response = client.table(self.TABLE).select("*").eq("is_active", True).execute()
            return [
                map_to_product(row)
                for row in response.data
                if int(row["stock"]) <= int(row.get("min_stock", 5))
            ]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list low stock: {e}")

    async def find_by_barcode(self, barcode: str) -> Product | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("barcode", barcode).execute()
            if not response.data:
                return None
            return map_to_product(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to find product by barcode: {e}")

    async def delete(self, product_id: UUID) -> None:
        try:
            client = await SupabaseClientSingleton.get_client()
            client.table(self.TABLE).delete().eq("id", str(product_id)).execute()
        except Exception as e:
            raise DatabaseError(f"Failed to delete product: {e}")
