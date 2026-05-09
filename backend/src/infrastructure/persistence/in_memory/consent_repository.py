"""In-memory consent repository for development and testing.

This module provides a simple in-memory implementation of the
ConsentRepository protocol. Stores consents in a dictionary,
useful for rapid development and unit testing.

Note: Data is NOT persisted between restarts. For production,
use the Supabase repository implementation.
"""

from uuid import UUID

from domain.entities.consent_entity import Consent
from domain.enums.consent_status import ConsentStatus
from domain.repositories.consent_repository import ConsentRepository


class InMemoryConsentRepository:
    """In-memory implementation of ConsentRepository.

    Stores Consent entities in a dictionary keyed by consent ID.
    Implements all methods defined by the ConsentRepository protocol.

    Attributes:
        _storage: Internal dictionary storing Consent entities.
    """

    def __init__(self) -> None:
        """Initialize with an empty consent store."""

        self._storage: dict[UUID, Consent] = {}


    async def get_by_id(self, consent_id: UUID) -> Consent | None:
        """Retrieve a consent by its unique identifier.

        Args:
            consent_id: The UUID of the consent to find.

        Returns:
            The Consent entity if found, None otherwise.
        """

        return self._storage.get(consent_id)


    async def save(self, consent: Consent) -> Consent:
        """Persist a consent entity (create or update).

        If the consent ID already exists, it is updated in place.
        Otherwise, it is stored as a new consent.

        Args:
            consent: The Consent entity to persist.

        Returns:
            The persisted Consent entity.
        """

        self._storage[consent.id] = consent

        return consent


    async def find_by_token(self, token: str) -> Consent | None:
        """Find a consent by its unique access token.

        Args:
            token: The unique URL-safe token.

        Returns:
            The Consent entity if found, None otherwise.
        """

        for consent in self._storage.values():
            if consent.token == token:
                return consent

        return None


    async def list_by_client(
        self,
        client_id: UUID,
        status: ConsentStatus | None = None,
    ) -> list[Consent]:
        """List all consents for a specific client.

        Args:
            client_id: The UUID of the client.
            status: Optional filter by consent status.

        Returns:
            A list of Consent entities for the client.
        """

        consents = [
            c
            for c in self._storage.values()
            if c.client_id == client_id
        ]

        if status is not None:
            consents = [c for c in consents if c.status == status]

        return consents


    async def list_all(
        self,
        client_id: UUID | None = None,
        status: ConsentStatus | None = None,
    ) -> list[Consent]:
        """List all consents in the system with optional filters.

        Args:
            client_id: Optional filter by client UUID.
            status: Optional filter by consent status.

        Returns:
            A list of Consent entities.
        """

        consents = list(self._storage.values())

        if client_id is not None:
            consents = [c for c in consents if c.client_id == client_id]

        if status is not None:
            consents = [c for c in consents if c.status == status]

        return consents
