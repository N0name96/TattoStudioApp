"""Client repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any client repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/in_memory/client_repository.py
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.client_entity import Client
from domain.enums.client_source import ClientSource


@runtime_checkable
class ClientRepository(Protocol):
    """Interface for Client persistence.

    This protocol defines the contract that any client repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer by the in-memory repository.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, client_id: UUID) -> Client | None:
        """Retrieve a client by its unique identifier.

        Args:
            client_id: The UUID of the client to find.

        Returns:
            The Client entity if found, None otherwise.
        """
        ...

    async def get_by_email(self, email: str) -> Client | None:
        """Retrieve a client by their email address.

        Used for uniqueness validation during creation.

        Args:
            email: The email address to search for.

        Returns:
            The Client entity if found, None otherwise.
        """
        ...

    async def save(self, client: Client) -> Client:
        """Persist a client entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            client: The Client entity to persist.

        Returns:
            The persisted Client entity.
        """
        ...

    async def list_all(
        self,
        is_active: bool | None = None,
        source: ClientSource | None = None,
    ) -> list[Client]:
        """List all clients with optional filters.

        Args:
            is_active: Optional filter for active/inactive clients.
            source: Optional filter by client source channel.

        Returns:
            A list of Client entities.
        """
        ...

    async def delete(self, client_id: UUID) -> None:
        """Remove a client by its unique identifier.

        Args:
            client_id: The UUID of the client to delete.
        """
        ...
