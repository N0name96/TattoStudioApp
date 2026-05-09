"""Tests for the LoginCommand."""

from unittest.mock import AsyncMock

import pytest

from application.commands.auth.login_command import LoginCommand
from application.dto.requests.auth.login_request import LoginRequest
from core.errors import UnauthorizedError
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
def valid_login_request():
    return LoginRequest(
        email="client@example.com",
        password="StrongPass123",
    )


class TestLoginCommand:
    @pytest.mark.asyncio
    async def test_login_success(self, mock_repo, security_service, valid_login_request):
        hashed_password = security_service.hash_password(valid_login_request.password)
        user = User.create(
            email=valid_login_request.email,
            hashed_password=hashed_password,
            full_name="Client User",
            role=UserRole.CLIENT,
        )

        mock_repo.get_by_email.return_value = user
        command = LoginCommand(mock_repo, security_service)

        tokens = await command.execute(valid_login_request)

        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type == "bearer"
        assert tokens.expires_in > 0

    @pytest.mark.asyncio
    async def test_login_invalid_password_raises(self, mock_repo, security_service, valid_login_request):
        hashed_password = security_service.hash_password("OtherPass123")
        user = User.create(
            email=valid_login_request.email,
            hashed_password=hashed_password,
            full_name="Client User",
            role=UserRole.CLIENT,
        )

        mock_repo.get_by_email.return_value = user
        command = LoginCommand(mock_repo, security_service)

        with pytest.raises(UnauthorizedError):
            await command.execute(valid_login_request)

    @pytest.mark.asyncio
    async def test_login_inactive_user_raises(self, mock_repo, security_service, valid_login_request):
        hashed_password = security_service.hash_password(valid_login_request.password)
        user = User.create(
            email=valid_login_request.email,
            hashed_password=hashed_password,
            full_name="Client User",
            role=UserRole.CLIENT,
        )
        user.deactivate()

        mock_repo.get_by_email.return_value = user
        command = LoginCommand(mock_repo, security_service)

        with pytest.raises(UnauthorizedError):
            await command.execute(valid_login_request)
