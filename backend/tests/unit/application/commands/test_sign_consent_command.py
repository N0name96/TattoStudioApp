"""Tests for the SignConsentCommand."""

from uuid import uuid4

import pytest

from application.commands.consents.sign_consent_command import (
    SignConsentCommand,
)
from application.dto.requests.consents.sign_consent_request import (
    SignConsentRequest,
)
from core.errors import BusinessRuleError, EntityNotFoundError
from domain.entities.consent_entity import Consent
from domain.enums.consent_type import ConsentType
from infrastructure.persistence.in_memory.consent_repository import (
    InMemoryConsentRepository,
)


class TestSignConsentCommand:
    """Tests for SignConsentCommand."""

    @pytest.fixture
    def consent_repo(self):
        return InMemoryConsentRepository()

    @pytest.fixture
    def command(self, consent_repo):
        return SignConsentCommand(consent_repo)

    @pytest.mark.asyncio
    async def test_sign_consent_success(self, command, consent_repo):
        """Test signing a pending consent."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )
        await consent_repo.save(consent)

        request = SignConsentRequest(signature_data="base64_signature_data")

        response = await command.execute(consent.id, request)

        assert response.status == "signed"
        assert response.signature_data == "base64_signature_data"
        assert response.signed_at is not None

    @pytest.mark.asyncio
    async def test_sign_nonexistent_consent_raises_error(self, command):
        """Test that signing a non-existent consent raises error."""

        request = SignConsentRequest(signature_data="base64_signature")

        with pytest.raises(EntityNotFoundError, match="not found"):
            await command.execute(uuid4(), request)

    @pytest.mark.asyncio
    async def test_sign_already_signed_consent_raises_error(
        self, command, consent_repo
    ):
        """Test that signing an already signed consent raises error."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )
        consent.sign(signature_data="base64_signature_1")
        await consent_repo.save(consent)

        request = SignConsentRequest(signature_data="base64_signature_2")

        with pytest.raises(BusinessRuleError):
            await command.execute(consent.id, request)
