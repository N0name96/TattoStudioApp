"""Tests for the Consent domain entity.

This module tests the pure business logic of the Consent entity,
including creation, state transitions, signature, expiry, renewal,
and validation rules.

No mocks are needed since the entity has no external dependencies.
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from core.errors import BusinessRuleError
from domain.entities.consent_entity import Consent, DEFAULT_CONSENT_VALIDITY_HOURS
from domain.enums.consent_status import ConsentStatus
from domain.enums.consent_type import ConsentType


class TestConsentCreation:
    """Tests for Consent.create() factory method."""

    def test_create_consent_with_valid_data(self):
        """Test that a valid consent can be created."""

        client_id = uuid4()

        consent = Consent.create(
            client_id=client_id,
            consent_type=ConsentType.TATTOO,
        )

        assert consent.client_id == client_id
        assert consent.consent_type == ConsentType.TATTOO
        assert consent.status == ConsentStatus.PENDING
        assert consent.appointment_id is None
        assert consent.token is not None
        assert len(consent.token) > 0
        assert consent.signature_data is None
        assert consent.signed_at is None
        assert consent.expires_at > datetime.now()

    def test_create_consent_with_appointment(self):
        """Test creating a consent linked to an appointment."""

        appointment_id = uuid4()

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.PIERCING,
            appointment_id=appointment_id,
        )

        assert consent.appointment_id == appointment_id

    def test_create_consent_generates_unique_token(self):
        """Test that each consent gets a unique token."""

        consent1 = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent2 = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.PIERCING,
        )

        assert consent1.token != consent2.token

    def test_create_consent_generates_unique_id(self):
        """Test that each consent gets a unique ID."""

        consent1 = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent2 = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        assert consent1.id != consent2.id

    def test_create_consent_sets_expiry(self):
        """Test that the consent expiry is set correctly."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
            validity_hours=48,
        )

        expected_expiry = consent.created_at + timedelta(hours=48)
        delta = abs((consent.expires_at - expected_expiry).total_seconds())

        assert delta < 1

    def test_create_consent_with_zero_validity_raises_error(self):
        """Test that zero validity hours raises BusinessRuleError."""

        with pytest.raises(BusinessRuleError, match="greater than zero"):
            Consent.create(
                client_id=uuid4(),
                consent_type=ConsentType.TATTOO,
                validity_hours=0,
            )

    def test_create_consent_with_negative_validity_raises_error(self):
        """Test that negative validity hours raises BusinessRuleError."""

        with pytest.raises(BusinessRuleError, match="greater than zero"):
            Consent.create(
                client_id=uuid4(),
                consent_type=ConsentType.TATTOO,
                validity_hours=-1,
            )


class TestConsentSign:
    """Tests for Consent.sign() method."""

    def test_sign_pending_consent(self):
        """Test signing a pending consent."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature_data")

        assert consent.status == ConsentStatus.SIGNED
        assert consent.signature_data == "base64_signature_data"
        assert consent.signed_at is not None
        assert consent.signed_at > consent.created_at

    def test_sign_already_signed_consent_raises_error(self):
        """Test that signing an already signed consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature_1")

        with pytest.raises(BusinessRuleError):
            consent.sign(signature_data="base64_signature_2")

    def test_sign_revoked_consent_raises_error(self):
        """Test that signing a revoked consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature")
        consent.revoke()

        with pytest.raises(BusinessRuleError):
            consent.sign(signature_data="another_signature")


class TestConsentRevoke:
    """Tests for Consent.revoke() method."""

    def test_revoke_signed_consent(self):
        """Test revoking a signed consent."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature")
        consent.revoke()

        assert consent.status == ConsentStatus.REVOKED

    def test_revoke_pending_consent_raises_error(self):
        """Test that revoking a pending consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        with pytest.raises(BusinessRuleError):
            consent.revoke()

    def test_revoke_already_revoked_consent_raises_error(self):
        """Test that revoking an already revoked consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature")
        consent.revoke()

        with pytest.raises(BusinessRuleError):
            consent.revoke()


class TestConsentExpire:
    """Tests for Consent.expire() method."""

    def test_expire_pending_consent(self):
        """Test expiring a pending consent."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.expire()

        assert consent.status == ConsentStatus.EXPIRED

    def test_expire_signed_consent_raises_error(self):
        """Test that expiring a signed consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature")

        with pytest.raises(BusinessRuleError):
            consent.expire()


class TestConsentRenew:
    """Tests for Consent.renew() method."""

    def test_renew_pending_consent(self):
        """Test renewing a pending consent extends expiry."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
            validity_hours=24,
        )

        original_expiry = consent.expires_at

        consent.renew(additional_hours=48)

        assert consent.expires_at > original_expiry
        expected = datetime.now() + timedelta(hours=48)
        delta = abs((consent.expires_at - expected).total_seconds())
        assert delta < 2

    def test_renew_signed_consent_raises_error(self):
        """Test that renewing a signed consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        consent.sign(signature_data="base64_signature")

        with pytest.raises(BusinessRuleError):
            consent.renew()

    def test_renew_with_zero_hours_raises_error(self):
        """Test that renewing with zero hours raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        with pytest.raises(BusinessRuleError, match="greater than zero"):
            consent.renew(additional_hours=0)


class TestConsentExpiryCheck:
    """Tests for Consent._is_expired() method."""

    def test_non_expired_consent(self):
        """Test that a newly created consent is not expired."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
            validity_hours=72,
        )

        assert consent._is_expired() is False

    def test_expired_consent(self):
        """Test that a consent with past expiry is expired."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
            validity_hours=72,
        )

        # Force the expiry to be in the past
        consent.expires_at = datetime.now() - timedelta(hours=1)

        assert consent._is_expired() is True

    def test_expired_consent_cannot_be_signed(self):
        """Test that signing an expired consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
            validity_hours=72,
        )

        # Force the expiry to be in the past
        consent.expires_at = datetime.now() - timedelta(hours=1)

        with pytest.raises(BusinessRuleError, match="Cannot sign an expired consent"):
            consent.sign(signature_data="base64_signature")
