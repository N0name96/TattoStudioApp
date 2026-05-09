"""Command to create a new artist in the TattoStudioApp.

This command handles the artist creation flow:
1. Check email uniqueness
2. Create the domain entity
3. Persist to repository
4. Return response DTO
"""

import logging

from application.dto.requests.artists.create_artist_request import (
    CreateArtistRequest,
)
from application.dto.responses.artists.artist_response import ArtistResponse
from core.errors import DuplicateEntityError
from domain.entities.artist_entity import Artist
from domain.repositories.artist_repository import ArtistRepository

logger = logging.getLogger(__name__)


class CreateArtistCommand:
    """Command to create a new artist and persist it.

    This command validates that the artist email is unique before creating
    the domain entity and persisting it.

    Attributes:
        _artist_repo: Repository for artist persistence.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the command with the artist repository.

        Args:
            artist_repo: Repository for artist persistence.
        """

        self._artist_repo = artist_repo

    async def execute(self, request: CreateArtistRequest) -> ArtistResponse:
        """Execute the artist creation flow.

        Steps:
            1. Check email uniqueness.
            2. Create the domain entity with business rules applied.
            3. Persist the artist.
            4. Return the response DTO.

        Args:
            request: Validated artist creation data.

        Returns:
            The created artist as a response DTO.

        Raises:
            DuplicateEntityError: If the email is already registered.
        """

        logger.info(
            "Creating artist",
            extra={
                "extra_data": {
                    "email": request.email,
                    "name": request.name,
                }
            },
        )

        # Step 1: Validate that the artist email is not already registered
        existing = await self._artist_repo.get_by_email(request.email)
        if existing is not None:
            raise DuplicateEntityError(
                f"Artist with email {request.email} already exists"
            )

        # Step 2: Create the artist entity from validated request data
        artist = Artist.create(
            name=request.name,
            specialty=request.specialty,
            email=request.email,
            phone=request.phone,
            bio=request.bio,
        )

        # Step 3: Persist the new artist
        saved = await self._artist_repo.save(artist)

        logger.info(
            "Artist created successfully",
            extra={
                "extra_data": {
                    "artist_id": str(saved.id),
                    "name": saved.name,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return ArtistResponse.model_validate(saved)
