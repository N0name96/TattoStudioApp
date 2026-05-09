"""Command to sign a consent in the TattoStudioApp.

This command handles the consent signing flow:
1. Retrieve the consent by ID
2. Apply the sign transition with signature data
3. Persist the updated entity
"""

import logging
from uuid import UUID

from application.dto.requests.consents.sign_consent_request import (
    SignConsentRequest,
)
from application.dto.responses.consents.consent_response import (
    ConsentResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.consent_repository import ConsentRepository

logger = logging.getLogger(__name__)


class SignConsentCommand:
    """Command to sign a consent document.

    Applies the sign transition on the domain entity with
    the client's signature data.

    Attributes:
        _consent_repo: Repository for consent persistence.
    """

    def __init__(self, consent_repo: ConsentRepository) -> None:
        """Initialize the command with the consent repository.

        Args:
            consent_repo: Repository for consent persistence.
        """

        self._consent_repo = consent_repo


    async def execute(
        self,
        consent_id: UUID,
        request: SignConsentRequest,
    ) -> ConsentResponse:
        """Execute the consent signing flow.

        Steps:
            1. Retrieve the consent.
            2. Apply the sign transition with signature data.
            3. Persist the updated entity.

        Args:
            consent_id: UUID of the consent to sign.
            request: Validated signing data with signature.

        Returns:
            The signed consent as a response DTO.

        Raises:
            EntityNotFoundError: If the consent does not exist.
        """

        logger.info(
            "Signing consent",
            extra={"extra_data": {"consent_id": str(consent_id)}},
        )

        # Step 1: Retrieve the consent
        consent = await self._consent_repo.get_by_id(consent_id)

        if consent is None:
            raise EntityNotFoundError(
                f"Consent {consent_id} not found"
            )

        # Step 2: Apply the sign transition
        consent.sign(signature_data=request.signature_data)

        # Step 3: Persist the updated entity
        saved = await self._consent_repo.save(consent)

        logger.info(
            "Consent signed successfully",
            extra={"extra_data": {"consent_id": str(saved.id)}},
        )

        return ConsentResponse.model_validate(saved)
