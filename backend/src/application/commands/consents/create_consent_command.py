"""Command to create a new consent document in the TattoStudioApp.

This command handles the consent creation flow:
1. Verify the client exists
2. Create the domain entity with unique token and expiry
3. Persist to repository
4. Return response DTO with token (for QR/link generation)
"""

import logging

from application.dto.requests.consents.create_consent_request import (
    CreateConsentRequest,
)
from application.dto.responses.consents.consent_response import (
    ConsentResponse,
)
from core.errors import EntityNotFoundError
from domain.entities.consent_entity import Consent
from domain.repositories.client_repository import ClientRepository
from domain.repositories.consent_repository import ConsentRepository

logger = logging.getLogger(__name__)


class CreateConsentCommand:
    """Command to create a new consent document.

    Generates a unique token for the client to access the consent
    via QR code or remote link.

    Attributes:
        _consent_repo: Repository for consent persistence.
        _client_repo: Repository for client lookups.
    """

    def __init__(
        self,
        consent_repo: ConsentRepository,
        client_repo: ClientRepository,
    ) -> None:
        """Initialize the command with required repositories.

        Args:
            consent_repo: Repository for consent persistence.
            client_repo: Repository for client lookups.
        """

        self._consent_repo = consent_repo
        self._client_repo = client_repo


    async def execute(
        self,
        request: CreateConsentRequest,
    ) -> ConsentResponse:
        """Execute the consent creation flow.

        Steps:
            1. Verify the client exists.
            2. Create the domain entity with unique token.
            3. Persist the consent.
            4. Return the response DTO.

        Args:
            request: Validated consent creation data.

        Returns:
            The created consent as a response DTO.

        Raises:
            EntityNotFoundError: If the client does not exist.
        """

        logger.info(
            "Creating consent",
            extra={
                "extra_data": {
                    "client_id": str(request.client_id),
                    "consent_type": request.consent_type.value,
                    "appointment_id": str(request.appointment_id) if request.appointment_id else None,
                }
            },
        )

        # Step 1: Verify the client exists
        client = await self._client_repo.get_by_id(request.client_id)

        if client is None:
            raise EntityNotFoundError(
                f"Client {request.client_id} not found"
            )

        # Step 2: Create the domain entity with business rules
        consent = Consent.create(
            client_id=request.client_id,
            consent_type=request.consent_type,
            appointment_id=request.appointment_id,
        )

        # Step 3: Persist the consent
        saved = await self._consent_repo.save(consent)

        logger.info(
            "Consent created successfully",
            extra={
                "extra_data": {
                    "consent_id": str(saved.id),
                    "token": saved.token,
                    "status": saved.status.value,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return ConsentResponse.model_validate(saved)
