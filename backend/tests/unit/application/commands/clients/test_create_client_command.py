"""Tests for the CreateClientCommand.

This module tests the client creation flow with mocked repositories
to isolate the command logic from infrastructure dependencies.
"""

from unittest.mock import AsyncMock

import pytest

from application.commands.clients.create_client_command import (
    CreateClientCommand,
)
from application.dto.requests.clients.create_client_request import (
    CreateClientRequest,
)
from core.errors import DuplicateEntityError
from domain.entities.client_entity import Client


@pytest.fixture
def mock_repo():
    """Create a mock client repository."""

    repo = AsyncMock()
    return repo


@pytest.fixture
def valid_request():
    """Create a valid client creation request."""

    return CreateClientRequest(
        full_name="John Doe",
        email="john@example.com",
        phone="+34123456789",
        allergies="None",
        notes="Test client",
    )


class TestCreateClientCommand:
    """Tests for CreateClientCommand.execute()."""

    @pytest.mark.asyncio
    async def test_create_client_success(self, mock_repo, valid_request):
        """Test successful client creation."""

        mock_repo.get_by_email.return_value = None
        mock_repo.save.side_effect = lambda c: c

        command = CreateClientCommand(mock_repo)
        response = await command.execute(valid_request)

        assert response.full_name == "John Doe"
        assert response.email == "john@example.com"
        assert response.phone == "+34123456789"
        assert response.is_active is True
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_client_checks_email(self, mock_repo, valid_request):
        """Test that email uniqueness is checked before creating."""

        mock_repo.get_by_email.return_value = None
        mock_repo.save.side_effect = lambda c: c

        command = CreateClientCommand(mock_repo)
        await command.execute(valid_request)

        mock_repo.get_by_email.assert_called_once_with("john@example.com")

    @pytest.mark.asyncio
    async def test_create_client_duplicate_email_raises(self, mock_repo, valid_request):
        """Test that duplicate email raises DuplicateEntityError."""

        existing_client = Client.create(
            full_name="Existing Client",
            email="john@example.com",
        )
        mock_repo.get_by_email.return_value = existing_client

        command = CreateClientCommand(mock_repo)

        with pytest.raises(DuplicateEntityError):
            await command.execute(valid_request)

    @pytest.mark.asyncio
    async def test_create_client_persists(self, mock_repo, valid_request):
        """Test that the client is saved to the repository."""

        mock_repo.get_by_email.return_value = None
        mock_repo.save.side_effect = lambda c: c

        command = CreateClientCommand(mock_repo)
        await command.execute(valid_request)

        mock_repo.save.assert_called_once()
        saved_client = mock_repo.save.call_args[0][0]
        assert isinstance(saved_client, Client)
        assert saved_client.full_name == "John Doe"
