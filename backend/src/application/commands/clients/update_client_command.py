"""Command to update an existing client in the TattoStudioApp.

This command handles the client update flow:
1. Find the client by ID
2. Apply profile updates
3. Persist changes
4. Return response DTO
"""

import logging
from uuid import UUID

from application.dto.requests.clients.update_client_request import (
    UpdateClientRequest,
)
from application.dto.responses.clients.client_response import (
    ClientResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)


class UpdateClientCommand:
    """Command to update an existing client profile.

    This command fetches the target client, applies the requested
    profile updates, and persists the changes.

    Attributes:
        _client_repo: Repository for client persistence.
    """

    def __init__(self, client_repo: ClientRepository) -> None:
        """Initialize the command with the client repository.

        Args:
            client_repo: Repository for client persistence.
        """

        self._client_repo = client_repo

    async def execute(
        self,
        client_id: UUID,
        request: UpdateClientRequest,
    ) -> ClientResponse:
        """Execute the client update flow.

        Steps:
            1. Find the client by ID.
            2. Apply profile updates (entity validates business rules).
            3. Persist the changes.
            4. Return the updated client.

        Args:
            client_id: UUID of the client to update.
            request: Validated update data.

        Returns:
            The updated client as a response DTO.

        Raises:
            EntityNotFoundError: If the client does not exist.
        """

        logger.info(
            "Updating client profile",
            extra={"extra_data": {"client_id": str(client_id)}},
        )

        # Step 1: Find the client
        client = await self._client_repo.get_by_id(client_id)
        if client is None:
            raise EntityNotFoundError(f"Client with id {client_id} was not found")

        # Step 2: Apply profile updates
        client.update_profile(
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            birth_date=request.birth_date,
            allergies=request.allergies,
            medical_conditions=request.medical_conditions,
            source=request.source,
            notes=request.notes,
        )

        # Step 3: Persist the changes
        saved = await self._client_repo.save(client)

        logger.info(
            "Client profile updated",
            extra={
                "extra_data": {
                    "client_id": str(saved.id),
                    "full_name": saved.full_name,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return ClientResponse.model_validate(saved)
