"""DTO init."""

from application.dto.requests.products.create_product_request import CreateProductRequest
from application.dto.requests.products.update_product_request import UpdateProductRequest
from application.dto.requests.products.update_stock_request import UpdateStockRequest
from application.dto.responses.products.product_response import ProductResponse

__all__ = [
    "CreateProductRequest",
    "ProductResponse",
    "UpdateProductRequest",
    "UpdateStockRequest",
]
