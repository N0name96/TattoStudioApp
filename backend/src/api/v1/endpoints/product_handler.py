"""API handler for product endpoints."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.products.create_product_request import CreateProductRequest
from application.dto.requests.products.update_product_request import UpdateProductRequest
from application.dto.requests.products.update_stock_request import UpdateStockRequest
from application.dto.responses.products.product_response import ProductResponse
from application.use_cases.products.product_use_case import ProductUseCase
from core.container import container
from core.errors import BusinessRuleError, EntityNotFoundError
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.product_category import ProductCategory
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


def get_product_use_case() -> ProductUseCase:
    return ProductUseCase(product_repo=container.product_repository)


@router.post("/", response_model=SuccessResponse[ProductResponse], status_code=status.HTTP_201_CREATED)
async def create_product(
    request: CreateProductRequest,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ProductResponse]:
    try:
        product = await use_case.create_product(request)
        return SuccessResponse(data=product, message="Product created successfully")
    except BusinessRuleError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e


@router.get("/{product_id}", response_model=SuccessResponse[ProductResponse])
async def get_product(
    product_id: UUID,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[ProductResponse]:
    try:
        product = await use_case.get_product(product_id)
        return SuccessResponse(data=product)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e


@router.get("/", response_model=SuccessResponse[list[ProductResponse]])
async def list_products(
    category: ProductCategory | None = None,
    active_only: bool = True,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[ProductResponse]]:
    products = await use_case.list_products(category=category, active_only=active_only)
    return SuccessResponse(data=products)


@router.get("/low-stock/", response_model=SuccessResponse[list[ProductResponse]])
async def list_low_stock(
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[list[ProductResponse]]:
    products = await use_case.list_low_stock()
    return SuccessResponse(data=products)


@router.put("/{product_id}", response_model=SuccessResponse[ProductResponse])
async def update_product(
    product_id: UUID,
    request: UpdateProductRequest,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ProductResponse]:
    try:
        product = await use_case.update_product(product_id, request)
        return SuccessResponse(data=product, message="Product updated successfully")
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except BusinessRuleError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e


@router.post("/{product_id}/stock/add", response_model=SuccessResponse[ProductResponse])
async def add_stock(
    product_id: UUID,
    request: UpdateStockRequest,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ProductResponse]:
    try:
        product = await use_case.add_stock(product_id, request.quantity)
        return SuccessResponse(data=product, message=f"Added {request.quantity} units")
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except BusinessRuleError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e


@router.post("/{product_id}/stock/remove", response_model=SuccessResponse[ProductResponse])
async def remove_stock(
    product_id: UUID,
    request: UpdateStockRequest,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ProductResponse]:
    try:
        product = await use_case.remove_stock(product_id, request.quantity)
        return SuccessResponse(data=product, message=f"Removed {request.quantity} units")
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except BusinessRuleError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    use_case: ProductUseCase = Depends(get_product_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> None:
    try:
        await use_case.delete_product(product_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
