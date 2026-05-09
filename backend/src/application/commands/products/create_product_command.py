"""Command to create a new product."""

import logging
from domain.value_objects.money_vo import Money
from application.dto.requests.products.create_product_request import CreateProductRequest
from application.dto.responses.products.product_response import ProductResponse
from domain.entities.product_entity import Product
from domain.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class CreateProductCommand:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(self, request: CreateProductRequest) -> ProductResponse:
        logger.info("Creating product", extra={"extra_data": {"name": request.name}})

        product = Product.create(
            name=request.name,
            category=request.category,
            price=Money(amount=request.price),
            cost_price=Money(amount=request.cost_price),
            stock=request.stock,
            min_stock=request.min_stock,
            description=request.description,
            barcode=request.barcode,
        )

        saved = await self._product_repo.save(product)

        logger.info("Product created", extra={"extra_data": {"product_id": str(saved.id)}})

        return ProductResponse(
            id=saved.id,
            name=saved.name,
            description=saved.description,
            category=saved.category,
            price=saved.price.amount,
            cost_price=saved.cost_price.amount,
            stock=saved.stock,
            min_stock=saved.min_stock,
            barcode=saved.barcode,
            is_active=saved.is_active,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
