"""Tests for the AuthUseCase orchestration."""

from unittest.mock import AsyncMock

import pytest

from application.dto.requests.auth.login_request import LoginRequest
from application.dto.requests.auth.refresh_token_request import RefreshTokenRequest
from application.dto.requests.auth.register_request import RegisterRequest
from application.use_cases.auth.auth_use_case import AuthUseCase
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
def valid_register_request():
    return RegisterRequest(
        email="client@example.com",
        password="StrongPass123",
        full_name="Client User",
        role=UserRole.CLIENT,
        phone="555-0100",
    )


@pytest.fixture
def valid_login_request():
    return LoginRequest(
        email="client@example.com",
        password="StrongPass123",
    )


@pytest.fixture
def valid_refresh_request(security_service, user):
    return RefreshTokenRequest(refresh_token=security_service.create_refresh_token(user_id=user.id))


@pytest.fixture
def user(security_service):
    return User.create(
        email="client@example.com",
        hashed_password=security_service.hash_password("StrongPass123"),
        full_name="Client User",
        role=UserRole.CLIENT,
    )


class TestAuthUseCase:
    @pytest.mark.asyncio
    async def test_register_delegates_to_command(self, mock_repo, security_service, valid_register_request):
        mock_repo.get_by_email.return_value = None
        mock_repo.save.side_effect = lambda user: user
        use_case = AuthUseCase(user_repo=mock_repo, security_service=security_service)

        response = await use_case.register(valid_register_request)

        assert response.email == valid_register_request.email
        mock_repo.get_by_email.assert_awaited_once_with(valid_register_request.email)
        mock_repo.save.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_login_delegates_to_command(self, mock_repo, security_service, valid_login_request, user):
        mock_repo.get_by_email.return_value = user
        use_case = AuthUseCase(user_repo=mock_repo, security_service=security_service)

        response = await use_case.login(valid_login_request)

        assert response.access_token
        assert response.refresh_token

    @pytest.mark.asyncio
    async def test_refresh_token_delegates_to_command(self, mock_repo, security_service, valid_refresh_request, user):
        mock_repo.get_by_id.return_value = user
        use_case = AuthUseCase(user_repo=mock_repo, security_service=security_service)

        response = await use_case.refresh_token(valid_refresh_request)

        assert response.access_token
        assert response.refresh_token
