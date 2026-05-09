"""Tests for the Client domain entity.

This module tests the pure business logic of the Client entity,
including creation, profile updates, image rights, and activation.

No mocks are needed since the entity has no external dependencies.
"""

from datetime import datetime

import pytest

from core.errors import BusinessRuleError
from domain.entities.client_entity import Client
from domain.enums.client_source import ClientSource
from domain.enums.image_rights import ImageRights


class TestClientCreation:
    """Tests for Client.create() factory method."""

    def test_create_client_with_valid_data(self):
        """Test that a valid client can be created."""

        client = Client.create(
            full_name="John Doe",
            email="john@example.com",
            phone="+34123456789",
            source=ClientSource.INSTAGRAM,
        )

        assert client.full_name == "John Doe"
        assert client.email == "john@example.com"
        assert client.phone == "+34123456789"
        assert client.source == ClientSource.INSTAGRAM
        assert client.is_active is True
        assert client.allergies == ""
        assert client.medical_conditions == ""
        assert client.notes == ""
        assert len(client.image_rights) == 0

    def test_create_client_generates_unique_id(self):
        """Test that each client gets a unique ID."""

        client1 = Client.create(
            full_name="Alice",
            email="alice@example.com",
        )

        client2 = Client.create(
            full_name="Bob",
            email="bob@example.com",
        )

        assert client1.id != client2.id

    def test_create_client_with_medical_info(self):
        """Test that medical information is stored."""

        client = Client.create(
            full_name="Jane Doe",
            email="jane@example.com",
            allergies="Latex, Penicillin",
            medical_conditions="Diabetes type 1",
        )

        assert client.allergies == "Latex, Penicillin"
        assert client.medical_conditions == "Diabetes type 1"

    def test_create_client_with_birth_date(self):
        """Test that birth date is stored."""

        birth_date = datetime(1990, 5, 15)

        client = Client.create(
            full_name="Sam Smith",
            email="sam@example.com",
            birth_date=birth_date,
        )

        assert client.birth_date == birth_date

    def test_create_client_defaults_active(self):
        """Test that a new client is active by default."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        assert client.is_active is True


class TestClientProfileUpdate:
    """Tests for Client.update_profile() method."""

    def test_update_profile_changes_fields(self):
        """Test that profile fields can be updated."""

        client = Client.create(
            full_name="Old Name",
            email="old@example.com",
            phone="+34000000000",
        )

        client.update_profile(
            full_name="New Name",
            email="new@example.com",
            phone="+34999999999",
            allergies="None",
            medical_conditions="None",
            notes="Important client",
        )

        assert client.full_name == "New Name"
        assert client.email == "new@example.com"
        assert client.phone == "+34999999999"
        assert client.allergies == "None"
        assert client.medical_conditions == "None"
        assert client.notes == "Important client"

    def test_update_profile_partial_update(self):
        """Test that only provided fields are updated."""

        client = Client.create(
            full_name="Original Name",
            email="original@example.com",
        )

        client.update_profile(full_name="Updated Name")

        assert client.full_name == "Updated Name"
        assert client.email == "original@example.com"

    def test_update_profile_updates_timestamp(self):
        """Test that update_profile updates the timestamp."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        original_updated_at = client.updated_at
        client.update_profile(full_name="Updated User")

        assert client.updated_at > original_updated_at

    def test_update_profile_with_source(self):
        """Test that source channel can be updated."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        client.update_profile(source=ClientSource.GOOGLE_MAPS)

        assert client.source == ClientSource.GOOGLE_MAPS


class TestImageRights:
    """Tests for client image rights management."""

    def test_grant_image_rights(self):
        """Test granting image rights."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        rights = {ImageRights.SOCIAL_MEDIA, ImageRights.PORTFOLIO}
        client.grant_image_rights(rights)

        assert client.image_rights == rights

    def test_revoke_image_rights(self):
        """Test revoking all image rights."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        rights = {ImageRights.SOCIAL_MEDIA, ImageRights.ADVERTISING}
        client.grant_image_rights(rights)
        client.revoke_image_rights()

        assert len(client.image_rights) == 0

    def test_image_rights_starts_empty(self):
        """Test that new clients have no image rights."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        assert len(client.image_rights) == 0


class TestClientActivation:
    """Tests for client activation/deactivation."""

    def test_deactivate_active_client(self):
        """Test deactivating an active client."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        client.deactivate()

        assert client.is_active is False

    def test_activate_inactive_client(self):
        """Test activating an inactive client."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        client.deactivate()
        client.activate()

        assert client.is_active is True

    def test_deactivate_already_inactive_raises(self):
        """Test deactivating an already inactive client raises error."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        client.deactivate()

        with pytest.raises(BusinessRuleError):
            client.deactivate()

    def test_activate_already_active_raises(self):
        """Test activating an already active client raises error."""

        client = Client.create(
            full_name="Test User",
            email="test@example.com",
        )

        with pytest.raises(BusinessRuleError):
            client.activate()
