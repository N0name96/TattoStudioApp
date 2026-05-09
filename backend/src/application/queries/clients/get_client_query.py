"""Query to retrieve a single client by id in the TattoStudioApp.

This module provides the query for fetching a single client
by their unique identifier.
"""

import logging
from uuid import UUID

from application.dto.responses.clients.client_response import ClientResponse
from core.errors import EntityNotFoundError
from domain.repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)


class GetClientQuery:
    """Query for fetching a client by unique identifier.

    This query retrieves a single client and maps it
    to the response DTO.

    Attributes:
        _client_repo: Repository for client persistence.
    """

    def __init__(self, client_repo: ClientRepository) -> None:
        """Initialize the query with the client repository.

        Args:
            client_repo: Repository for client persistence.
        """

        self._client_repo = client_repo

    async def execute(self, client_id: UUID) -> ClientResponse:
        """Execute the get client query.

        Retrieves the requested client and converts the domain entity
        into the response DTO.

        Args:
            client_id: UUID of the client to retrieve.

        Returns:
            The client as a response DTO.

        Raises:
            EntityNotFoundError: If the client does not exist.
        """

        logger.debug(
            "Fetching client",
            extra={"extra_data": {"client_id": str(client_id)}},
        )

        # Step 1: Find the client
        client = await self._client_repo.get_by_id(client_id)
        if client is None:
            raise EntityNotFoundError(f"Client with id {client_id} was not found")

        # Step 2: Map domain entity to response DTO
        return ClientResponse.model_validate(client)
