"""Tests for the RegisterCommand."""

from unittest.mock import AsyncMock

import pytest

from application.commands.auth.register_command import RegisterCommand
from application.dto.requests.auth.register_request import RegisterRequest
from core.errors import DuplicateEntityError
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


class TestRegisterCommand:
    @pytest.mark.asyncio
    async def test_register_success(self, mock_repo, security_service, valid_register_request):
        mock_repo.get_by_email.return_value = None
        mock_repo.save.side_effect = lambda user: user

        command = RegisterCommand(mock_repo, security_service)
        response = await command.execute(valid_register_request)

        assert response.email == valid_register_request.email
        assert response.full_name == valid_register_request.full_name
        assert response.role == valid_register_request.role
        assert response.phone == valid_register_request.phone
        mock_repo.get_by_email.assert_awaited_once_with(valid_register_request.email)
        mock_repo.save.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises(self, mock_repo, security_service, valid_register_request):
        mock_repo.get_by_email.return_value = object()

        command = RegisterCommand(mock_repo, security_service)

        with pytest.raises(DuplicateEntityError):
            await command.execute(valid_register_request)
