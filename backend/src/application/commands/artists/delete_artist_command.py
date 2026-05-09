"""Command to delete an artist in the TattoStudioApp.

This command handles artist deletion:
1. Verify the artist exists
2. Delete from repository
"""

import logging
from uuid import UUID

from core.errors import EntityNotFoundError
from domain.repositories.artist_repository import ArtistRepository

logger = logging.getLogger(__name__)


class DeleteArtistCommand:
    """Command to remove an artist from persistence.

    This command verifies the artist exists before requesting removal.

    Attributes:
        _artist_repo: Repository for artist persistence.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the command with the artist repository.

        Args:
            artist_repo: Repository for artist persistence.
        """

        self._artist_repo = artist_repo

    async def execute(self, artist_id: UUID) -> None:
        """Execute the delete artist flow.

        Steps:
            1. Find the artist by ID.
            2. Delete from repository.

        Args:
            artist_id: UUID of the artist to delete.

        Raises:
            EntityNotFoundError: If the artist does not exist.
        """

        logger.info(
            "Deleting artist",
            extra={"extra_data": {"artist_id": str(artist_id)}},
        )

        # Step 1: Find the artist
        artist = await self._artist_repo.get_by_id(artist_id)
        if artist is None:
            raise EntityNotFoundError(f"Artist with id {artist_id} was not found")

        # Step 2: Delete from repository
        await self._artist_repo.delete(artist_id)

        logger.info(
            "Artist deleted",
            extra={"extra_data": {"artist_id": str(artist_id)}},
        )
