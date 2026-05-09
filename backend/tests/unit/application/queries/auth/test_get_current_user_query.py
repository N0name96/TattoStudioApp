"""Tests for the GetCurrentUserQuery."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.queries.auth.get_current_user_query import GetCurrentUserQuery
from core.errors import EntityNotFoundError
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def user(security_service=None):
    return User.create(
        email="client@example.com",
        hashed_password="hashed-password",
        full_name="Client User",
        role=UserRole.CLIENT,
    )


class TestGetCurrentUserQuery:
    @pytest.mark.asyncio
    async def test_execute_returns_user(self, mock_repo, user):
        mock_repo.get_by_id.return_value = user
        query = GetCurrentUserQuery(mock_repo)

        response = await query.execute(user.id)

        assert response.id == user.id
        assert response.email == user.email
        assert response.role == user.role

    @pytest.mark.asyncio
    async def test_execute_raises_if_user_not_found(self, mock_repo):
        mock_repo.get_by_id.return_value = None
        query = GetCurrentUserQuery(mock_repo)

        with pytest.raises(EntityNotFoundError):
            await query.execute(uuid4())
