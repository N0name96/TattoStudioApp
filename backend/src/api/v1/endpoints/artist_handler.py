"""API handler for artist endpoints.

This module provides the FastAPI router for artist operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.artists.create_artist_request import (
    CreateArtistRequest,
)
from application.dto.requests.artists.update_artist_request import (
    UpdateArtistRequest,
)
from application.dto.responses.artists.artist_response import ArtistResponse
from application.use_cases.artists.artist_use_case import ArtistUseCase
from core.container import container
from core.errors import EntityNotFoundError
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/artists", tags=["artists"])


def get_artist_use_case() -> ArtistUseCase:
    """Provide the ArtistUseCase dependency for artist endpoints.

    The use case is resolved from the application container and encapsulates
    the artist business logic for create/read/update/delete operations.

    Returns:
        An ArtistUseCase instance.
    """

    return ArtistUseCase(artist_repo=container.artist_repository)


@router.post(
    "/",
    response_model=SuccessResponse[ArtistResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_artist(
    request: CreateArtistRequest,
    use_case: ArtistUseCase = Depends(get_artist_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ArtistResponse]:
    """Create a new artist.

    Only admins can create artists.

    Args:
        request: Validated artist creation data.
        use_case: Injected use case for artist operations.
        current_user: Authenticated admin user.

    Returns:
        A success response containing the created artist.

    Raises:
        HTTPException: 409 if email already exists, 422 if validation fails.
    """

    artist = await use_case.create_artist(request)

    return SuccessResponse(
        data=artist,
        message="Artist created successfully",
    )


@router.get(
    "/",
    response_model=SuccessResponse[list[ArtistResponse]],
)
async def list_artists(
    is_active: bool | None = None,
    use_case: ArtistUseCase = Depends(get_artist_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[ArtistResponse]]:
    """List artists with optional active status filter.

    All authenticated users can list artists.

    Args:
        is_active: Optional filter for active/inactive artists.
        use_case: Injected use case for artist operations.
        current_user: Authenticated user.

    Returns:
        A success response containing a list of artists.
    """

    artists = await use_case.list_artists(is_active=is_active)
    return SuccessResponse(data=artists)


@router.get(
    "/{artist_id}",
    response_model=SuccessResponse[ArtistResponse],
)
async def get_artist(
    artist_id: UUID,
    use_case: ArtistUseCase = Depends(get_artist_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[ArtistResponse]:
    """Retrieve an artist by its unique identifier.

    Args:
        artist_id: The UUID of the artist to retrieve.
        use_case: Injected use case for artist operations.
        current_user: Authenticated user.

    Returns:
        A success response containing the artist data.

    Raises:
        HTTPException: 404 if the artist is not found.
    """

    try:
        artist = await use_case.get_artist(artist_id)
        return SuccessResponse(data=artist)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{artist_id}",
    response_model=SuccessResponse[ArtistResponse],
)
async def update_artist(
    artist_id: UUID,
    request: UpdateArtistRequest,
    use_case: ArtistUseCase = Depends(get_artist_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ArtistResponse]:
    """Update an existing artist profile.

    Only admins can update artists.

    Args:
        artist_id: The UUID of the artist to update.
        request: Validated update data.
        use_case: Injected use case for artist operations.
        current_user: Authenticated admin user.

    Returns:
        A success response containing the updated artist.

    Raises:
        HTTPException: 404 if the artist is not found.
    """

    try:
        artist = await use_case.update_artist(artist_id, request)
        return SuccessResponse(
            data=artist,
            message="Artist updated successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete(
    "/{artist_id}",
    response_model=SuccessResponse[None],
)
async def delete_artist(
    artist_id: UUID,
    use_case: ArtistUseCase = Depends(get_artist_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[None]:
    """Delete an artist.

    Only admins can delete artists.

    Args:
        artist_id: The UUID of the artist to delete.
        use_case: Injected use case for artist operations.
        current_user: Authenticated admin user.

    Returns:
        A success response with no data.

    Raises:
        HTTPException: 404 if the artist is not found.
    """

    try:
        await use_case.delete_artist(artist_id)
        return SuccessResponse(
            data=None,
            message="Artist deleted successfully",
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
