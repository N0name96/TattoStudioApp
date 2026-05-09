"""Tests for the CreateConsentCommand."""

from uuid import uuid4

import pytest

from application.commands.consents.create_consent_command import (
    CreateConsentCommand,
)
from application.dto.requests.consents.create_consent_request import (
    CreateConsentRequest,
)
from core.errors import EntityNotFoundError
from domain.entities.client_entity import Client
from domain.enums.consent_status import ConsentStatus
from domain.enums.consent_type import ConsentType
from infrastructure.persistence.in_memory.client_repository import (
    InMemoryClientRepository,
)
from infrastructure.persistence.in_memory.consent_repository import (
    InMemoryConsentRepository,
)


class TestCreateConsentCommand:
    """Tests for CreateConsentCommand."""

    @pytest.fixture
    def consent_repo(self):
        return InMemoryConsentRepository()

    @pytest.fixture
    def client_repo(self):
        return InMemoryClientRepository()

    @pytest.fixture
    def command(self, consent_repo, client_repo):
        return CreateConsentCommand(consent_repo, client_repo)

    @pytest.mark.asyncio
    async def test_create_consent_success(self, command, client_repo):
        """Test creating a consent for an existing client."""

        client = Client.create(
            full_name="Test Client",
            email="test@example.com",
            phone="+34600000000",
        )
        await client_repo.save(client)

        request = CreateConsentRequest(
            client_id=client.id,
            consent_type=ConsentType.TATTOO,
        )

        response = await command.execute(request)

        assert response.id is not None
        assert response.client_id == client.id
        assert response.consent_type == ConsentType.TATTOO
        assert response.status == ConsentStatus.PENDING
        assert response.token is not None
        assert len(response.token) > 0
        assert response.signature_data is None

    @pytest.mark.asyncio
    async def test_create_consent_client_not_found_raises_error(self, command):
        """Test that creating a consent for a non-existent client fails."""

        request = CreateConsentRequest(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )

        with pytest.raises(EntityNotFoundError, match="not found"):
            await command.execute(request)

    @pytest.mark.asyncio
    async def test_create_consent_is_persisted(
        self, command, consent_repo, client_repo
    ):
        """Test that the created consent is actually persisted."""

        client = Client.create(
            full_name="Test Client",
            email="test@example.com",
            phone="+34600000000",
        )
        await client_repo.save(client)

        request = CreateConsentRequest(
            client_id=client.id,
            consent_type=ConsentType.PIERCING,
        )

        response = await command.execute(request)

        persisted = await consent_repo.get_by_id(response.id)
        assert persisted is not None
        assert persisted.consent_type == ConsentType.PIERCING

    @pytest.mark.asyncio
    async def test_create_consent_with_appointment(
        self, command, client_repo
    ):
        """Test creating a consent linked to an appointment."""

        client = Client.create(
            full_name="Test Client",
            email="test@example.com",
            phone="+34600000000",
        )
        await client_repo.save(client)

        appointment_id = uuid4()

        request = CreateConsentRequest(
            client_id=client.id,
            consent_type=ConsentType.TATTOO,
            appointment_id=appointment_id,
        )

        response = await command.execute(request)

        assert response.appointment_id == appointment_id
