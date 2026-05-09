"""Query to retrieve a single artist by id in the TattoStudioApp.

This module provides the query for fetching a single artist
by their unique identifier.
"""

import logging
from uuid import UUID

from application.dto.responses.artists.artist_response import ArtistResponse
from core.errors import EntityNotFoundError
from domain.repositories.artist_repository import ArtistRepository

logger = logging.getLogger(__name__)


class GetArtistQuery:
    """Query for fetching an artist by unique identifier.

    This query retrieves a single artist and maps it
    to the response DTO.

    Attributes:
        _artist_repo: Repository for artist persistence.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the query with the artist repository.

        Args:
            artist_repo: Repository for artist persistence.
        """

        self._artist_repo = artist_repo

    async def execute(self, artist_id: UUID) -> ArtistResponse:
        """Execute the get artist query.

        Retrieves the requested artist and converts the domain entity into the
        response DTO.

        Args:
            artist_id: UUID of the artist to retrieve.

        Returns:
            The artist as a response DTO.

        Raises:
            EntityNotFoundError: If the artist does not exist.
        """

        logger.debug(
            "Fetching artist",
            extra={"extra_data": {"artist_id": str(artist_id)}},
        )

        # Step 1: Find the artist
        artist = await self._artist_repo.get_by_id(artist_id)
        if artist is None:
            raise EntityNotFoundError(f"Artist with id {artist_id} was not found")

        # Step 2: Map domain entity to response DTO
        return ArtistResponse.model_validate(artist)
