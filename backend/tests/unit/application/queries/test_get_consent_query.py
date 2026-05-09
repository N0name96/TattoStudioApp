"""Tests for the GetConsentQuery."""

from uuid import uuid4

import pytest

from application.queries.consents.get_consent_query import GetConsentQuery
from core.errors import EntityNotFoundError
from domain.entities.consent_entity import Consent
from domain.enums.consent_type import ConsentType
from infrastructure.persistence.in_memory.consent_repository import (
    InMemoryConsentRepository,
)


class TestGetConsentQuery:
    """Tests for GetConsentQuery."""

    @pytest.fixture
    def consent_repo(self):
        return InMemoryConsentRepository()

    @pytest.fixture
    def query(self, consent_repo):
        return GetConsentQuery(consent_repo)

    @pytest.mark.asyncio
    async def test_get_existing_consent(self, query, consent_repo):
        """Test retrieving an existing consent."""

        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.TATTOO,
        )
        await consent_repo.save(consent)

        response = await query.execute(consent.id)

        assert response.id == consent.id
        assert response.consent_type == ConsentType.TATTOO
        assert response.token == consent.token

    @pytest.mark.asyncio
    async def test_get_consent_by_token(self):
        """Test retrieving a consent by its token."""

        repo = InMemoryConsentRepository()
        consent = Consent.create(
            client_id=uuid4(),
            consent_type=ConsentType.LASER,
        )
        await repo.save(consent)

        found = await repo.find_by_token(consent.token)

        assert found is not None
        assert found.id == consent.id

    @pytest.mark.asyncio
    async def test_get_nonexistent_consent_raises_error(self, query):
        """Test that retrieving a non-existent consent raises error."""

        with pytest.raises(EntityNotFoundError, match="not found"):
            await query.execute(uuid4())
