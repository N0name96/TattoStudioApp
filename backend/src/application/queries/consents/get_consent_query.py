"""Query to retrieve a single consent by ID."""

import logging
from uuid import UUID

from application.dto.responses.consents.consent_response import (
    ConsentResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.consent_repository import ConsentRepository

logger = logging.getLogger(__name__)


class GetConsentQuery:
    """Query to retrieve a single consent by ID.

    This query handles the read operation for consent data,
    mapping from domain entity to response DTO.

    Attributes:
        _consent_repo: Repository for consent lookups.
    """

    def __init__(self, consent_repo: ConsentRepository) -> None:
        """Initialize the query with the consent repository.

        Args:
            consent_repo: Repository for consent lookups.
        """

        self._consent_repo = consent_repo


    async def execute(self, consent_id: UUID) -> ConsentResponse:
        """Execute the consent retrieval.

        Args:
            consent_id: The unique identifier of the consent.

        Returns:
            The consent data as a response DTO.

        Raises:
            EntityNotFoundError: If the consent does not exist.
        """

        consent = await self._consent_repo.get_by_id(consent_id)

        if consent is None:
            raise EntityNotFoundError(f"Consent {consent_id} not found")

        return ConsentResponse.model_validate(consent)
