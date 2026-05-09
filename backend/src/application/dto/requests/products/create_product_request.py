"""Request DTO for creating a product."""

from decimal import Decimal

from pydantic import BaseModel, Field

from domain.enums.product_category import ProductCategory


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: ProductCategory
    price: Decimal = Field(gt=0)
    cost_price: Decimal = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    min_stock: int = Field(default=5, ge=0)
    description: str | None = Field(default=None, max_length=500)
    barcode: str | None = Field(default=None, max_length=50)
