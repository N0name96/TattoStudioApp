"""Command to update an existing artist in the TattoStudioApp.

This command handles the artist update flow:
1. Find the artist by ID
2. Apply profile updates
3. Persist changes
4. Return response DTO
"""

import logging
from uuid import UUID

from application.dto.requests.artists.update_artist_request import (
    UpdateArtistRequest,
)
from application.dto.responses.artists.artist_response import ArtistResponse
from core.errors import EntityNotFoundError
from domain.repositories.artist_repository import ArtistRepository

logger = logging.getLogger(__name__)


class UpdateArtistCommand:
    """Command to update an existing artist profile.

    This command fetches the target artist, applies the requested
    profile updates, and persists the changes.

    Attributes:
        _artist_repo: Repository for artist persistence.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the command with the artist repository.

        Args:
            artist_repo: Repository for artist persistence.
        """

        self._artist_repo = artist_repo

    async def execute(
        self,
        artist_id: UUID,
        request: UpdateArtistRequest,
    ) -> ArtistResponse:
        """Execute the artist update flow.

        Steps:
            1. Find the artist by ID.
            2. Apply profile updates (entity validates business rules).
            3. Persist the changes.
            4. Return the updated artist.

        Args:
            artist_id: UUID of the artist to update.
            request: Validated update data.

        Returns:
            The updated artist as a response DTO.

        Raises:
            EntityNotFoundError: If the artist does not exist.
        """

        logger.info(
            "Updating artist profile",
            extra={"extra_data": {"artist_id": str(artist_id)}},
        )

        # Step 1: Find the artist
        artist = await self._artist_repo.get_by_id(artist_id)
        if artist is None:
            raise EntityNotFoundError(f"Artist with id {artist_id} was not found")

        # Step 2: Apply profile updates
        artist.update_profile(
            name=request.name,
            specialty=request.specialty,
            email=request.email,
            phone=request.phone,
            bio=request.bio,
            is_active=request.is_active,
        )

        # Step 3: Persist the changes
        saved = await self._artist_repo.save(artist)

        logger.info(
            "Artist profile updated",
            extra={
                "extra_data": {
                    "artist_id": str(saved.id),
                    "name": saved.name,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return ArtistResponse.model_validate(saved)
