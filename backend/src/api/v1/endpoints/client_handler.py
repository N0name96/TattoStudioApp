"""API handler for client endpoints.

This module provides the FastAPI router for client operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.clients.create_client_request import (
    CreateClientRequest,
)
from application.dto.requests.clients.update_client_request import (
    UpdateClientRequest,
)
from application.dto.responses.clients.client_response import ClientResponse
from application.use_cases.clients.client_use_case import ClientUseCase
from core.container import container
from core.errors import DuplicateEntityError, EntityNotFoundError
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.client_source import ClientSource
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_use_case() -> ClientUseCase:
    """Provide the ClientUseCase dependency for client endpoints.

    The use case is resolved from the application container and encapsulates
    the client business logic for create/read/update/delete operations.

    Returns:
        A ClientUseCase instance.
    """

    return ClientUseCase(client_repo=container.client_repository)


@router.post(
    "/",
    response_model=SuccessResponse[ClientResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_client(
    request: CreateClientRequest,
    use_case: ClientUseCase = Depends(get_client_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[ClientResponse]:
    """Create a new client.

    All authenticated users can create clients.

    Args:
        request: Validated client creation data.
        use_case: Injected use case for client operations.
        current_user: Authenticated user.

    Returns:
        A success response containing the created client.

    Raises:
        HTTPException: 409 if email already exists, 422 if validation fails.
    """

    try:
        client = await use_case.create_client(request)

        return SuccessResponse(
            data=client,
            message="Client created successfully",
        )
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "/",
    response_model=SuccessResponse[list[ClientResponse]],
)
async def list_clients(
    is_active: bool | None = Query(default=None),
    source: ClientSource | None = Query(default=None),
    use_case: ClientUseCase = Depends(get_client_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[ClientResponse]]:
    """List clients with optional filters.

    All authenticated users can list clients.

    Args:
        is_active: Optional filter for active/inactive clients.
        source: Optional filter by client source channel.
        use_case: Injected use case for client operations.
        current_user: Authenticated user.

    Returns:
        A success response containing a list of clients.
    """

    clients = await use_case.list_clients(
        is_active=is_active,
        source=source,
    )
    return SuccessResponse(data=clients)


@router.get(
    "/{client_id}",
    response_model=SuccessResponse[ClientResponse],
)
async def get_client(
    client_id: UUID,
    use_case: ClientUseCase = Depends(get_client_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[ClientResponse]:
    """Retrieve a client by its unique identifier.

    Args:
        client_id: The UUID of the client to retrieve.
        use_case: Injected use case for client operations.
        current_user: Authenticated user.

    Returns:
        A success response containing the client data.

    Raises:
        HTTPException: 404 if the client is not found.
    """

    try:
        client = await use_case.get_client(client_id)
        return SuccessResponse(data=client)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{client_id}",
    response_model=SuccessResponse[ClientResponse],
)
async def update_client(
    client_id: UUID,
    request: UpdateClientRequest,
    use_case: ClientUseCase = Depends(get_client_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[ClientResponse]:
    """Update an existing client profile.

    All authenticated users can update client profiles.

    Args:
        client_id: The UUID of the client to update.
        request: Validated update data.
        use_case: Injected use case for client operations.
        current_user: Authenticated user.

    Returns:
        A success response containing the updated client.

    Raises:
        HTTPException: 404 if the client is not found.
    """

    try:
        client = await use_case.update_client(client_id, request)
        return SuccessResponse(
            data=client,
            message="Client updated successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete(
    "/{client_id}",
    response_model=SuccessResponse[None],
)
async def delete_client(
    client_id: UUID,
    use_case: ClientUseCase = Depends(get_client_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[None]:
    """Delete a client.

    Only admins can delete clients.

    Args:
        client_id: The UUID of the client to delete.
        use_case: Injected use case for client operations.
        current_user: Authenticated admin user.

    Returns:
        A success response with no data.

    Raises:
        HTTPException: 404 if the client is not found.
    """

    try:
        await use_case.delete_client(client_id)
        return SuccessResponse(
            data=None,
            message="Client deleted successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
