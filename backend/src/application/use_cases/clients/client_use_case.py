"""Use case for client operations in the TattoStudioApp.

This module provides a high-level interface for client operations,
orchestrating commands and queries. It acts as the entry point for
the API layer to interact with the clients domain.
"""

from uuid import UUID

from application.commands.clients.create_client_command import CreateClientCommand
from application.commands.clients.delete_client_command import DeleteClientCommand
from application.commands.clients.update_client_command import UpdateClientCommand
from application.dto.requests.clients.create_client_request import CreateClientRequest
from application.dto.requests.clients.update_client_request import UpdateClientRequest
from application.dto.responses.clients.client_response import ClientResponse
from application.queries.clients.get_client_query import GetClientQuery
from application.queries.clients.list_clients_query import ListClientsQuery
from domain.enums.client_source import ClientSource
from domain.repositories.client_repository import ClientRepository


class ClientUseCase:
    """Use case for client operations.

    Orchestrates commands and queries for the clients module.
    Provides a single entry point for the API layer.

    Attributes:
        _client_repo: Repository for client persistence.
        _create_command: Command for creating clients.
        _update_command: Command for updating clients.
        _delete_command: Command for deleting clients.
        _get_query: Query for retrieving a single client.
        _list_query: Query for listing clients.
    """

    def __init__(self, client_repo: ClientRepository) -> None:
        """Initialize the use case with the client repository.

        Args:
            client_repo: Repository for client persistence.
        """

        self._client_repo = client_repo
        self._create_command = CreateClientCommand(client_repo)
        self._update_command = UpdateClientCommand(client_repo)
        self._delete_command = DeleteClientCommand(client_repo)
        self._get_query = GetClientQuery(client_repo)
        self._list_query = ListClientsQuery(client_repo)

    async def create_client(self, request: CreateClientRequest) -> ClientResponse:
        """Create a new client.

        Args:
            request: Validated client creation data.

        Returns:
            The created client as a response DTO.
        """

        return await self._create_command.execute(request)

    async def get_client(self, client_id: UUID) -> ClientResponse:
        """Retrieve a single client by its identifier.

        Args:
            client_id: UUID of the client to retrieve.

        Returns:
            The client as a response DTO.
        """

        return await self._get_query.execute(client_id)

    async def list_clients(
        self,
        is_active: bool | None = None,
        source: ClientSource | None = None,
    ) -> list[ClientResponse]:
        """List clients with optional filters.

        Args:
            is_active: Optional filter for active/inactive clients.
            source: Optional filter by client source channel.

        Returns:
            A list of client response DTOs.
        """

        return await self._list_query.execute(
            is_active=is_active,
            source=source,
        )

    async def update_client(
        self, client_id: UUID, request: UpdateClientRequest
    ) -> ClientResponse:
        """Update an existing client profile.

        Args:
            client_id: UUID of the client to update.
            request: Validated update data.

        Returns:
            The updated client as a response DTO.
        """

        return await self._update_command.execute(client_id, request)

    async def delete_client(self, client_id: UUID) -> None:
        """Delete a client by its identifier.

        Args:
            client_id: UUID of the client to delete.
        """

        await self._delete_command.execute(client_id)
