"""Artist repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any artist repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/in_memory/artist_repository.py
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.artist_entity import Artist


@runtime_checkable
class ArtistRepository(Protocol):
    """Interface for Artist persistence.

    This protocol defines the contract that any artist repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer by the in-memory repository.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        """Retrieve an artist by its unique identifier.

        Args:
            artist_id: The UUID of the artist to find.

        Returns:
            The Artist entity if found, None otherwise.
        """
        ...

    async def get_by_email(self, email: str) -> Artist | None:
        """Retrieve an artist by their email address.

        Used for uniqueness validation during creation.

        Args:
            email: The email address to search for.

        Returns:
            The Artist entity if found, None otherwise.
        """
        ...

    async def save(self, artist: Artist) -> Artist:
        """Persist an artist entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            artist: The Artist entity to persist.

        Returns:
            The persisted Artist entity.
        """
        ...

    async def list_all(self, is_active: bool | None = None) -> list[Artist]:
        """List all artists with optional active status filter.

        Args:
            is_active: Optional filter for active/inactive artists.

        Returns:
            A list of Artist entities.
        """
        ...

    async def delete(self, artist_id: UUID) -> None:
        """Remove an artist by its unique identifier.

        Args:
            artist_id: The UUID of the artist to delete.
        """
        ...
