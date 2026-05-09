"""Command to create a new client in the TattoStudioApp.

This command handles the client creation flow:
1. Check email uniqueness
2. Create the domain entity
3. Persist to repository
4. Return response DTO
"""

import logging

from application.dto.requests.clients.create_client_request import (
    CreateClientRequest,
)
from application.dto.responses.clients.client_response import (
    ClientResponse,
)
from core.errors import DuplicateEntityError
from domain.entities.client_entity import Client
from domain.repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)


class CreateClientCommand:
    """Command to create a new client and persist it.

    This command validates that the client email is unique before creating
    the domain entity and persisting it.

    Attributes:
        _client_repo: Repository for client persistence.
    """

    def __init__(self, client_repo: ClientRepository) -> None:
        """Initialize the command with the client repository.

        Args:
            client_repo: Repository for client persistence.
        """

        self._client_repo = client_repo

    async def execute(self, request: CreateClientRequest) -> ClientResponse:
        """Execute the client creation flow.

        Steps:
            1. Check email uniqueness.
            2. Create the domain entity with business rules applied.
            3. Persist the client.
            4. Return the response DTO.

        Args:
            request: Validated client creation data.

        Returns:
            The created client as a response DTO.

        Raises:
            DuplicateEntityError: If the email is already registered.
        """

        logger.info(
            "Creating client",
            extra={
                "extra_data": {
                    "email": request.email,
                    "full_name": request.full_name,
                }
            },
        )

        # Step 1: Validate that the client email is not already registered
        existing = await self._client_repo.get_by_email(request.email)
        if existing is not None:
            raise DuplicateEntityError(
                f"Client with email {request.email} already exists"
            )

        # Step 2: Create the client entity from validated request data
        client = Client.create(
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            birth_date=request.birth_date,
            allergies=request.allergies,
            medical_conditions=request.medical_conditions,
            source=request.source,
            notes=request.notes,
        )

        # Step 3: Persist the new client
        saved = await self._client_repo.save(client)

        logger.info(
            "Client created successfully",
            extra={
                "extra_data": {
                    "client_id": str(saved.id),
                    "full_name": saved.full_name,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return ClientResponse.model_validate(saved)
