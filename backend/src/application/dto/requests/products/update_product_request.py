"""Request DTO for updating a product."""

from decimal import Decimal

from pydantic import BaseModel, Field

from domain.enums.product_category import ProductCategory


class UpdateProductRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    category: ProductCategory | None = None
    price: Decimal | None = Field(default=None, gt=0)
    cost_price: Decimal | None = Field(default=None, ge=0)
    min_stock: int | None = Field(default=None, ge=0)
    barcode: str | None = Field(default=None, max_length=50)
