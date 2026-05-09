"""Use case for artist operations in the TattoStudioApp.

This module provides a high-level interface for artist operations,
orchestrating commands and queries. It acts as the entry point for
the API layer to interact with the artists domain.
"""

from uuid import UUID

from application.commands.artists.create_artist_command import CreateArtistCommand
from application.commands.artists.delete_artist_command import DeleteArtistCommand
from application.commands.artists.update_artist_command import UpdateArtistCommand
from application.dto.requests.artists.create_artist_request import CreateArtistRequest
from application.dto.requests.artists.update_artist_request import UpdateArtistRequest
from application.dto.responses.artists.artist_response import ArtistResponse
from application.queries.artists.get_artist_query import GetArtistQuery
from application.queries.artists.list_artists_query import ListArtistsQuery
from domain.repositories.artist_repository import ArtistRepository


class ArtistUseCase:
    """Use case for artist operations.

    Orchestrates commands and queries for the artists module.
    Provides a single entry point for the API layer.

    Attributes:
        _artist_repo: Repository for artist persistence.
        _create_command: Command for creating artists.
        _update_command: Command for updating artists.
        _delete_command: Command for deleting artists.
        _get_query: Query for retrieving a single artist.
        _list_query: Query for listing artists.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the use case with the artist repository.

        Args:
            artist_repo: Repository for artist persistence.
        """

        self._artist_repo = artist_repo
        self._create_command = CreateArtistCommand(artist_repo)
        self._update_command = UpdateArtistCommand(artist_repo)
        self._delete_command = DeleteArtistCommand(artist_repo)
        self._get_query = GetArtistQuery(artist_repo)
        self._list_query = ListArtistsQuery(artist_repo)

    async def create_artist(self, request: CreateArtistRequest) -> ArtistResponse:
        """Create a new artist.

        Args:
            request: Validated artist creation data.

        Returns:
            The created artist as a response DTO.
        """

        return await self._create_command.execute(request)

    async def get_artist(self, artist_id: UUID) -> ArtistResponse:
        """Retrieve a single artist by its identifier.

        Args:
            artist_id: UUID of the artist to retrieve.

        Returns:
            The artist as a response DTO.
        """

        return await self._get_query.execute(artist_id)

    async def list_artists(self, is_active: bool | None = None) -> list[ArtistResponse]:
        """List artists with optional active status filtering.

        Args:
            is_active: Optional filter for active/inactive artists.

        Returns:
            A list of artist response DTOs.
        """

        return await self._list_query.execute(is_active=is_active)

    async def update_artist(
        self, artist_id: UUID, request: UpdateArtistRequest
    ) -> ArtistResponse:
        """Update an existing artist profile.

        Args:
            artist_id: UUID of the artist to update.
            request: Validated update data.

        Returns:
            The updated artist as a response DTO.
        """

        return await self._update_command.execute(artist_id, request)

    async def delete_artist(self, artist_id: UUID) -> None:
        """Delete an artist by its identifier.

        Args:
            artist_id: UUID of the artist to delete.
        """

        await self._delete_command.execute(artist_id)
