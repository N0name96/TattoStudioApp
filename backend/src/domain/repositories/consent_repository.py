"""Consent repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any consent repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/supabase/consent_repository.py
    - infrastructure/persistence/in_memory/consent_repository.py
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.consent_entity import Consent
from domain.enums.consent_status import ConsentStatus


@runtime_checkable
class ConsentRepository(Protocol):
    """Interface for Consent persistence.

    This protocol defines the contract that any consent repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, consent_id: UUID) -> Consent | None:
        """Retrieve a consent by its unique identifier.

        Args:
            consent_id: The UUID of the consent to find.

        Returns:
            The Consent entity if found, None otherwise.
        """
        ...


    async def save(self, consent: Consent) -> Consent:
        """Persist a consent entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            consent: The Consent entity to persist.

        Returns:
            The persisted Consent entity.
        """
        ...


    async def find_by_token(self, token: str) -> Consent | None:
        """Find a consent by its unique access token.

        Used when clients access the consent via QR code or remote link.

        Args:
            token: The unique URL-safe token.

        Returns:
            The Consent entity if found, None otherwise.
        """
        ...


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
        ...


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
        ...
