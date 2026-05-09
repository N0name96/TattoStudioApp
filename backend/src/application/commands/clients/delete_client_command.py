"""Command to delete a client in the TattoStudioApp.

This command handles client deletion:
1. Verify the client exists
2. Delete from repository
"""

import logging
from uuid import UUID

from core.errors import EntityNotFoundError
from domain.repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)


class DeleteClientCommand:
    """Command to remove a client from persistence.

    This command verifies the client exists before requesting removal.

    Attributes:
        _client_repo: Repository for client persistence.
    """

    def __init__(self, client_repo: ClientRepository) -> None:
        """Initialize the command with the client repository.

        Args:
            client_repo: Repository for client persistence.
        """

        self._client_repo = client_repo

    async def execute(self, client_id: UUID) -> None:
        """Execute the delete client flow.

        Steps:
            1. Find the client by ID.
            2. Delete from repository.

        Args:
            client_id: UUID of the client to delete.

        Raises:
            EntityNotFoundError: If the client does not exist.
        """

        logger.info(
            "Deleting client",
            extra={"extra_data": {"client_id": str(client_id)}},
        )

        # Step 1: Find the client
        client = await self._client_repo.get_by_id(client_id)
        if client is None:
            raise EntityNotFoundError(f"Client with id {client_id} was not found")

        # Step 2: Delete from repository
        await self._client_repo.delete(client_id)

        logger.info(
            "Client deleted",
            extra={"extra_data": {"client_id": str(client_id)}},
        )
