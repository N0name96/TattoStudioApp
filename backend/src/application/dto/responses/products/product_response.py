"""Response DTO for product data."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.enums.product_category import ProductCategory


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    category: ProductCategory
    price: Decimal
    cost_price: Decimal
    stock: int
    min_stock: int
    barcode: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
