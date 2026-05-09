"""Tests for the SecurityService implementation."""

from uuid import uuid4

import pytest

from core.errors import UnauthorizedError
from infrastructure.security.security_service import SecurityService


class TestSecurityService:
    """Tests for password hashing and JWT token handling."""

    @pytest.fixture
    def security_service(self) -> SecurityService:
        return SecurityService()

    def test_hash_and_verify_password(self, security_service: SecurityService):
        password = "MySecurePassword123"
        hashed = security_service.hash_password(password)

        assert hashed != password
        assert security_service.verify_password(password, hashed)
        assert not security_service.verify_password("wrong-password", hashed)

    def test_create_and_decode_access_token(self, security_service: SecurityService):
        user_id = uuid4()
        access_token = security_service.create_access_token(user_id=user_id, role="client")

        payload = security_service.decode_token(access_token)

        assert payload["sub"] == str(user_id)
        assert payload["role"] == "client"
        assert payload["type"] == "access"

    def test_create_and_decode_refresh_token(self, security_service: SecurityService):
        user_id = uuid4()
        refresh_token = security_service.create_refresh_token(user_id=user_id)

        payload = security_service.decode_token(refresh_token)

        assert payload["sub"] == str(user_id)
        assert payload["type"] == "refresh"

    def test_decode_invalid_token_raises_unauthorized(self, security_service: SecurityService):
        with pytest.raises(UnauthorizedError):
            security_service.decode_token("not-a-valid-jwt-token")
