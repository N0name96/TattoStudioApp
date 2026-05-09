"""Tests for the Email value object.

This module tests the pure business logic of the Email value object,
including format validation and immutability.
"""

import pytest

from domain.value_objects.email_vo import Email


class TestEmailCreation:
    """Tests for Email creation and validation."""

    def test_create_email_with_valid_format(self):
        """Test that an Email with a valid format can be created."""

        email = Email(value="artist@studio.com")

        assert email.value == "artist@studio.com"

    def test_create_email_with_subdomain(self):
        """Test that an Email with a subdomain is valid."""

        email = Email(value="contact@mail.studio.com")

        assert email.value == "contact@mail.studio.com"

    def test_create_email_with_plus_sign(self):
        """Test that an Email with a plus sign is valid."""

        email = Email(value="user+tag@studio.com")

        assert email.value == "user+tag@studio.com"

    def test_create_email_with_dots_in_local_part(self):
        """Test that an Email with dots in the local part is valid."""

        email = Email(value="first.last@studio.com")

        assert email.value == "first.last@studio.com"

    def test_create_email_without_at_symbol_raises_error(self):
        """Test that an Email without @ raises ValueError."""

        with pytest.raises(ValueError, match="Invalid email format"):
            Email(value="notanemail")

    def test_create_email_without_domain_raises_error(self):
        """Test that an Email without domain raises ValueError."""

        with pytest.raises(ValueError, match="Invalid email format"):
            Email(value="user@")

    def test_create_email_without_local_part_raises_error(self):
        """Test that an Email without local part raises ValueError."""

        with pytest.raises(ValueError, match="Invalid email format"):
            Email(value="@studio.com")

    def test_create_email_with_empty_string_raises_error(self):
        """Test that an empty string raises ValueError."""

        with pytest.raises(ValueError, match="Invalid email format"):
            Email(value="")

    def test_create_email_with_spaces_raises_error(self):
        """Test that an email with spaces raises ValueError."""

        with pytest.raises(ValueError, match="Invalid email format"):
            Email(value="user name@studio.com")


class TestEmailString:
    """Tests for Email.__str__() method."""

    def test_string_representation(self):
        """Test that __str__ returns the email value."""

        email = Email(value="artist@studio.com")

        assert str(email) == "artist@studio.com"


class TestEmailImmutability:
    """Tests for Email immutability (frozen dataclass)."""

    def test_email_is_immutable(self):
        """Test that Email cannot be modified after creation."""

        email = Email(value="artist@studio.com")

        with pytest.raises(Exception):
            email.value = "other@studio.com"
