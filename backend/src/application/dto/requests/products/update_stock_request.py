"""Request DTO for updating product stock."""

from pydantic import BaseModel, Field


class UpdateStockRequest(BaseModel):
    quantity: int = Field(gt=0)
