"""Tests for the UpdateClientCommand."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.commands.clients.update_client_command import (
    UpdateClientCommand,
)
from application.dto.requests.clients.update_client_request import (
    UpdateClientRequest,
)
from core.errors import EntityNotFoundError
from domain.entities.client_entity import Client


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def existing_client():
    return Client.create(
        full_name="Original Name",
        email="original@example.com",
    )


class TestUpdateClientCommand:
    """Tests for UpdateClientCommand.execute()."""

    @pytest.mark.asyncio
    async def test_update_client_success(self, mock_repo, existing_client):
        """Test successful client update."""

        mock_repo.get_by_id.return_value = existing_client
        mock_repo.save.side_effect = lambda c: c

        request = UpdateClientRequest(full_name="Updated Name")
        command = UpdateClientCommand(mock_repo)
        response = await command.execute(existing_client.id, request)

        assert response.full_name == "Updated Name"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_client_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised for nonexistent client."""

        mock_repo.get_by_id.return_value = None

        request = UpdateClientRequest(full_name="Updated Name")
        command = UpdateClientCommand(mock_repo)

        with pytest.raises(EntityNotFoundError):
            await command.execute(uuid4(), request)

    @pytest.mark.asyncio
    async def test_update_client_partial(self, mock_repo, existing_client):
        """Test partial update only changes provided fields."""

        mock_repo.get_by_id.return_value = existing_client
        mock_repo.save.side_effect = lambda c: c

        request = UpdateClientRequest(notes="New notes")
        command = UpdateClientCommand(mock_repo)
        response = await command.execute(existing_client.id, request)

        assert response.full_name == "Original Name"
        assert response.notes == "New notes"
