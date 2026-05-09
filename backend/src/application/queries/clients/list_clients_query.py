"""Query to list clients with optional filters in the TattoStudioApp.

This module provides the query for listing clients
with optional filtering by active status and source.
"""

import logging

from application.dto.responses.clients.client_response import ClientResponse
from domain.enums.client_source import ClientSource
from domain.repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)


class ListClientsQuery:
    """Query to list all clients or filter by status and source.

    This query retrieves all clients matching the provided
    filters and maps them to response DTOs.

    Attributes:
        _client_repo: Repository for client persistence.
    """

    def __init__(self, client_repo: ClientRepository) -> None:
        """Initialize the query with the client repository.

        Args:
            client_repo: Repository for client persistence.
        """

        self._client_repo = client_repo

    async def execute(
        self,
        is_active: bool | None = None,
        source: ClientSource | None = None,
    ) -> list[ClientResponse]:
        """Execute the list clients query.

        Returns clients filtered by their active status and/or source
        when requested.

        Args:
            is_active: Optional filter for active/inactive clients.
            source: Optional filter by client source channel.

        Returns:
            A list of client response DTOs.
        """

        logger.debug(
            "Listing clients",
            extra={"extra_data": {"is_active": is_active, "source": source}},
        )

        # Step 1: Fetch clients from repository with filters
        clients = await self._client_repo.list_all(
            is_active=is_active,
            source=source,
        )

        # Step 2: Map domain entities to response DTOs
        return [ClientResponse.model_validate(client) for client in clients]
