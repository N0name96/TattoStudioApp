"""In-memory implementation of the ArtistRepository.

This module provides a non-persistent repository for development
and testing purposes. Data is stored in memory and lost on restart.

Usage:
    from infrastructure.persistence.in_memory.artist_repository import (
        InMemoryArtistRepository,
    )
    repo = InMemoryArtistRepository()
"""

import logging
from uuid import UUID

from domain.entities.artist_entity import Artist

logger = logging.getLogger(__name__)


class InMemoryArtistRepository:
    """In-memory Artist repository for development and testing.

    Stores artists in a dictionary for development and testing.
    Data is lost when the application restarts.

    Attributes:
        _storage: Dictionary mapping artist IDs to entities.
        _email_index: Dictionary mapping emails to artist IDs for fast lookup.
    """

    def __init__(self) -> None:
        """Initialize the in-memory storage."""

        self._storage: dict[UUID, Artist] = {}
        self._email_index: dict[str, UUID] = {}

        logger.info("InMemoryArtistRepository initialized")

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        """Retrieve an artist by its unique ID.

        Args:
            artist_id: The UUID of the artist to find.

        Returns:
            The Artist entity if found, None otherwise.
        """

        return self._storage.get(artist_id)

    async def get_by_email(self, email: str) -> Artist | None:
        """Retrieve an artist by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The Artist entity if found, None otherwise.
        """

        artist_id = self._email_index.get(email)

        if artist_id is None:
            return None

        return self._storage.get(artist_id)

    async def save(self, artist: Artist) -> Artist:
        """Persist an artist entity (create or update).

        Args:
            artist: The Artist entity to persist.

        Returns:
            The persisted Artist entity.
        """

        self._storage[artist.id] = artist
        self._email_index[artist.email] = artist.id

        logger.debug(
            "Artist saved",
            extra={"extra_data": {"artist_id": str(artist.id)}},
        )

        return artist

    async def list_all(self, is_active: bool | None = None) -> list[Artist]:
        """List all artists with optional active status filter.

        Args:
            is_active: Optional filter for active/inactive artists.

        Returns:
            A list of Artist entities.
        """

        results = list(self._storage.values())

        if is_active is not None:
            results = [artist for artist in results if artist.is_active == is_active]

        return sorted(results, key=lambda artist: artist.created_at)

    async def delete(self, artist_id: UUID) -> None:
        """Remove an artist by its unique identifier.

        Args:
            artist_id: The UUID of the artist to delete.
        """

        artist = self._storage.pop(artist_id, None)

        if artist is not None:
            self._email_index.pop(artist.email, None)
