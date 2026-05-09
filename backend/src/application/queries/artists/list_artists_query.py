"""Query to list artists with optional active status filtering in the TattoStudioApp.

This module provides the query for listing artists
with optional filtering by active status.
"""

import logging

from application.dto.responses.artists.artist_response import ArtistResponse
from domain.repositories.artist_repository import ArtistRepository

logger = logging.getLogger(__name__)


class ListArtistsQuery:
    """Query to list all artists or only active/inactive artists.

    This query retrieves all artists matching the provided
    active status filter and maps them to response DTOs.

    Attributes:
        _artist_repo: Repository for artist persistence.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the query with the artist repository.

        Args:
            artist_repo: Repository for artist persistence.
        """

        self._artist_repo = artist_repo

    async def execute(self, is_active: bool | None = None) -> list[ArtistResponse]:
        """Execute the list artists query.

        Returns artists filtered by their active status when requested.

        Args:
            is_active: Optional filter for active/inactive artists.

        Returns:
            A list of artist response DTOs.
        """

        logger.debug(
            "Listing artists",
            extra={"extra_data": {"is_active": is_active}},
        )

        # Step 1: Fetch artists from repository with filter
        artists = await self._artist_repo.list_all(is_active=is_active)

        # Step 2: Map domain entities to response DTOs
        return [ArtistResponse.model_validate(artist) for artist in artists]
