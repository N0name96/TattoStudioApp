"""Tests for the DeleteClientCommand."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.commands.clients.delete_client_command import (
    DeleteClientCommand,
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
        full_name="Test Client",
        email="test@example.com",
    )


class TestDeleteClientCommand:
    """Tests for DeleteClientCommand.execute()."""

    @pytest.mark.asyncio
    async def test_delete_client_success(self, mock_repo, existing_client):
        """Test successful client deletion."""

        mock_repo.get_by_id.return_value = existing_client

        command = DeleteClientCommand(mock_repo)
        await command.execute(existing_client.id)

        mock_repo.delete.assert_called_once_with(existing_client.id)

    @pytest.mark.asyncio
    async def test_delete_client_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised for nonexistent client."""

        mock_repo.get_by_id.return_value = None

        command = DeleteClientCommand(mock_repo)

        with pytest.raises(EntityNotFoundError):
            await command.execute(uuid4())
