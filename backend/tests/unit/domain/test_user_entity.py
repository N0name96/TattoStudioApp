"""Tests for the User domain entity."""

from datetime import datetime
from uuid import UUID

import pytest

from core.errors import BusinessRuleError
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole


class TestUserEntity:
    """Tests for User entity business rules."""

    def test_create_sets_defaults(self):
        user = User.create(
            email="jane.doe@example.com",
            hashed_password="hashed-password",
            full_name="Jane Doe",
            role=UserRole.CLIENT,
            phone="555-1234",
        )

        assert isinstance(user.id, UUID)
        assert user.email == "jane.doe@example.com"
        assert user.hashed_password == "hashed-password"
        assert user.full_name == "Jane Doe"
        assert user.role == UserRole.CLIENT
        assert user.phone == "555-1234"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.created_at == user.updated_at

    def test_deactivate_and_activate(self):
        user = User.create(
            email="jane.doe@example.com",
            hashed_password="hashed-password",
            full_name="Jane Doe",
            role=UserRole.CLIENT,
        )

        user.deactivate()
        assert user.is_active is False

        user.activate()
        assert user.is_active is True

    def test_deactivate_when_already_inactive_raises(self):
        user = User.create(
            email="jane.doe@example.com",
            hashed_password="hashed-password",
            full_name="Jane Doe",
            role=UserRole.CLIENT,
        )

        user.deactivate()

        with pytest.raises(BusinessRuleError):
            user.deactivate()

    def test_update_profile_changes_mutable_fields(self):
        user = User.create(
            email="jane.doe@example.com",
            hashed_password="hashed-password",
            full_name="Jane Doe",
            role=UserRole.CLIENT,
            phone="555-1234",
        )

        user.update_profile(full_name="Jane Doe Jr.", phone="555-5678")

        assert user.full_name == "Jane Doe Jr."
        assert user.phone == "555-5678"
        assert user.updated_at >= user.created_at
