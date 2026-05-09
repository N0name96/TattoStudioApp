"""Tests for the ClientUseCase delegation."""

from unittest.mock import AsyncMock

import pytest

from application.dto.requests.clients.create_client_request import (
    CreateClientRequest,
)
from application.dto.requests.clients.update_client_request import (
    UpdateClientRequest,
)
from application.use_cases.clients.client_use_case import ClientUseCase
from domain.entities.client_entity import Client


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    return repo


class TestClientUseCase:
    """Tests for ClientUseCase method delegation."""

    @pytest.mark.asyncio
    async def test_create_client_delegates_to_command(self, mock_repo):
        """Test that create_client delegates to the create command."""

        use_case = ClientUseCase(mock_repo)
        request = CreateClientRequest(
            full_name="Test User",
            email="test@example.com",
        )

        mock_repo.get_by_email.return_value = None
        mock_repo.save.side_effect = lambda c: c

        response = await use_case.create_client(request)

        assert response.full_name == "Test User"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_client_delegates_to_query(self, mock_repo):
        """Test that get_client delegates to the get query."""

        use_case = ClientUseCase(mock_repo)
        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        mock_repo.get_by_id.return_value = client

        response = await use_case.get_client(client.id)

        assert response.full_name == "Test User"
        mock_repo.get_by_id.assert_called_once_with(client.id)

    @pytest.mark.asyncio
    async def test_list_clients_delegates_to_query(self, mock_repo):
        """Test that list_clients delegates to the list query."""

        use_case = ClientUseCase(mock_repo)
        mock_repo.list_all.return_value = []

        response = await use_case.list_clients()

        assert response == []
        mock_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_client_delegates_to_command(self, mock_repo):
        """Test that update_client delegates to the update command."""

        use_case = ClientUseCase(mock_repo)
        client = Client.create(
            full_name="Old Name",
            email="old@example.com",
        )

        mock_repo.get_by_id.return_value = client
        mock_repo.save.side_effect = lambda c: c

        request = UpdateClientRequest(full_name="New Name")
        response = await use_case.update_client(client.id, request)

        assert response.full_name == "New Name"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_client_delegates_to_command(self, mock_repo):
        """Test that delete_client delegates to the delete command."""

        use_case = ClientUseCase(mock_repo)
        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        mock_repo.get_by_id.return_value = client

        await use_case.delete_client(client.id)

        mock_repo.delete.assert_called_once_with(client.id)
