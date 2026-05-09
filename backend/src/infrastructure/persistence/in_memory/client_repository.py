"""In-memory implementation of the ClientRepository.

This module provides a non-persistent repository for development
and testing purposes. Data is stored in memory and lost on restart.

Usage:
    from infrastructure.persistence.in_memory.client_repository import (
        InMemoryClientRepository,
    )
    repo = InMemoryClientRepository()
"""

import logging
from uuid import UUID

from domain.entities.client_entity import Client
from domain.enums.client_source import ClientSource

logger = logging.getLogger(__name__)


class InMemoryClientRepository:
    """In-memory Client repository for development and testing.

    Stores clients in a dictionary for development and testing.
    Data is lost when the application restarts.

    Attributes:
        _storage: Dictionary mapping client IDs to entities.
        _email_index: Dictionary mapping emails to client IDs for fast lookup.
    """

    def __init__(self) -> None:
        """Initialize the in-memory storage."""

        self._storage: dict[UUID, Client] = {}
        self._email_index: dict[str, UUID] = {}

        logger.info("InMemoryClientRepository initialized")

    async def get_by_id(self, client_id: UUID) -> Client | None:
        """Retrieve a client by its unique ID.

        Args:
            client_id: The UUID of the client to find.

        Returns:
            The Client entity if found, None otherwise.
        """

        return self._storage.get(client_id)

    async def get_by_email(self, email: str) -> Client | None:
        """Retrieve a client by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The Client entity if found, None otherwise.
        """

        client_id = self._email_index.get(email)

        if client_id is None:
            return None

        return self._storage.get(client_id)

    async def save(self, client: Client) -> Client:
        """Persist a client entity (create or update).

        Args:
            client: The Client entity to persist.

        Returns:
            The persisted Client entity.
        """

        self._storage[client.id] = client
        self._email_index[client.email] = client.id

        logger.debug(
            "Client saved",
            extra={"extra_data": {"client_id": str(client.id)}},
        )

        return client

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

        results = list(self._storage.values())

        if is_active is not None:
            results = [c for c in results if c.is_active == is_active]

        if source is not None:
            results = [c for c in results if c.source == source]

        return sorted(results, key=lambda c: c.full_name)

    async def delete(self, client_id: UUID) -> None:
        """Remove a client by its unique identifier.

        Args:
            client_id: The UUID of the client to delete.
        """

        client = self._storage.pop(client_id, None)

        if client is not None:
            self._email_index.pop(client.email, None)
