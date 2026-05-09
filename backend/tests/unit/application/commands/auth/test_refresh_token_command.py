"""Tests for the RefreshTokenCommand."""

from unittest.mock import AsyncMock

import pytest

from application.commands.auth.refresh_token_command import RefreshTokenCommand
from application.dto.requests.auth.refresh_token_request import RefreshTokenRequest
from core.errors import EntityNotFoundError, UnauthorizedError
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole
from infrastructure.security.security_service import SecurityService


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def security_service():
    return SecurityService()


@pytest.fixture
def user(security_service: SecurityService):
    return User.create(
        email="client@example.com",
        hashed_password=security_service.hash_password("StrongPass123"),
        full_name="Client User",
        role=UserRole.CLIENT,
    )


@pytest.fixture
def valid_refresh_request(security_service: SecurityService, user: User):
    return RefreshTokenRequest(refresh_token=security_service.create_refresh_token(user_id=user.id))


class TestRefreshTokenCommand:
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, mock_repo, security_service, user, valid_refresh_request):
        mock_repo.get_by_id.return_value = user
        command = RefreshTokenCommand(mock_repo, security_service)

        response = await command.execute(valid_refresh_request)

        assert response.access_token
        assert response.refresh_token
        assert response.token_type == "bearer"
        assert response.expires_in > 0

    @pytest.mark.asyncio
    async def test_refresh_token_invalid_type_raises(self, mock_repo, security_service, user):
        access_token = security_service.create_access_token(user_id=user.id, role=user.role.value)
        request = RefreshTokenRequest(refresh_token=access_token)
        command = RefreshTokenCommand(mock_repo, security_service)

        with pytest.raises(UnauthorizedError):
            await command.execute(request)

    @pytest.mark.asyncio
    async def test_refresh_token_user_not_found_raises(self, mock_repo, security_service, user, valid_refresh_request):
        mock_repo.get_by_id.return_value = None
        command = RefreshTokenCommand(mock_repo, security_service)

        with pytest.raises(EntityNotFoundError):
            await command.execute(valid_refresh_request)
