"""Tests for the GetClientQuery."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.queries.clients.get_client_query import GetClientQuery
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


class TestGetClientQuery:
    """Tests for GetClientQuery.execute()."""

    @pytest.mark.asyncio
    async def test_get_client_success(self, mock_repo, existing_client):
        """Test successful client retrieval."""

        mock_repo.get_by_id.return_value = existing_client

        query = GetClientQuery(mock_repo)
        response = await query.execute(existing_client.id)

        assert response.full_name == "Test Client"
        assert response.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_client_not_found(self, mock_repo):
        """Test that EntityNotFoundError is raised for nonexistent client."""

        mock_repo.get_by_id.return_value = None

        query = GetClientQuery(mock_repo)

        with pytest.raises(EntityNotFoundError):
            await query.execute(uuid4())
