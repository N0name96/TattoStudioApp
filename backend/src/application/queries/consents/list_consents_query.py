"""Query to list consents with optional filters."""

import logging
from uuid import UUID

from application.dto.responses.consents.consent_response import (
    ConsentResponse,
)
from domain.enums.consent_status import ConsentStatus
from domain.repositories.consent_repository import ConsentRepository

logger = logging.getLogger(__name__)


class ListConsentsQuery:
    """Query to list consents with optional filters.

    This query handles listing consent records, supporting
    filtering by client or by consent status.

    Attributes:
        _consent_repo: Repository for consent lookups.
    """

    def __init__(self, consent_repo: ConsentRepository) -> None:
        """Initialize the query with the consent repository.

        Args:
            consent_repo: Repository for consent lookups.
        """

        self._consent_repo = consent_repo


    async def execute(
        self,
        client_id: UUID | None = None,
        status: ConsentStatus | None = None,
    ) -> list[ConsentResponse]:
        """Execute the consent listing.

        Args:
            client_id: Optional filter by client UUID.
            status: Optional filter by consent status.

        Returns:
            A list of consent response DTOs.
        """

        consents = await self._consent_repo.list_all(
            client_id=client_id,
            status=status,
        )

        return [ConsentResponse.model_validate(c) for c in consents]
