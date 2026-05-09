"""Use case for consent operations in the TattoStudioApp.

This module provides a high-level interface for consent operations,
orchestrating commands and queries.
"""

import logging
from uuid import UUID

from application.commands.consents.create_consent_command import (
    CreateConsentCommand,
)
from application.commands.consents.revoke_consent_command import (
    RevokeConsentCommand,
)
from application.commands.consents.sign_consent_command import (
    SignConsentCommand,
)
from application.dto.requests.consents.create_consent_request import (
    CreateConsentRequest,
)
from application.dto.requests.consents.sign_consent_request import (
    SignConsentRequest,
)
from application.dto.responses.consents.consent_response import (
    ConsentResponse,
)
from application.queries.consents.get_consent_query import (
    GetConsentQuery,
)
from application.queries.consents.list_consents_query import (
    ListConsentsQuery,
)
from domain.enums.consent_status import ConsentStatus
from domain.repositories.client_repository import ClientRepository
from domain.repositories.consent_repository import ConsentRepository
from core.errors import EntityNotFoundError

logger = logging.getLogger(__name__)


class ConsentUseCase:
    """Use case for consent operations.

    Orchestrates commands and queries for the consents module.
    Provides a single entry point for the API layer.

    Attributes:
        _consent_repo: Repository for consent persistence.
        _client_repo: Repository for client lookups.
        _create_command: Command for creating consents.
        _sign_command: Command for signing consents.
        _revoke_command: Command for revoking consents.
        _get_query: Query for retrieving a single consent.
        _list_query: Query for listing consents.
    """

    def __init__(
        self,
        consent_repo: ConsentRepository,
        client_repo: ClientRepository,
    ) -> None:
        """Initialize the use case with required repositories.

        Args:
            consent_repo: Repository for consent persistence.
            client_repo: Repository for client lookups.
        """

        self._consent_repo = consent_repo
        self._client_repo = client_repo
        self._create_command = CreateConsentCommand(consent_repo, client_repo)
        self._sign_command = SignConsentCommand(consent_repo)
        self._revoke_command = RevokeConsentCommand(consent_repo)
        self._get_query = GetConsentQuery(consent_repo)
        self._list_query = ListConsentsQuery(consent_repo)


    async def create_consent(
        self,
        request: CreateConsentRequest,
    ) -> ConsentResponse:
        """Create a new consent document.

        Args:
            request: Validated consent creation data.

        Returns:
            The created consent as a response DTO.
        """

        return await self._create_command.execute(request)


    async def get_consent(self, consent_id: UUID) -> ConsentResponse:
        """Retrieve a single consent by ID.

        Args:
            consent_id: UUID of the consent to retrieve.

        Returns:
            The consent as a response DTO.
        """

        return await self._get_query.execute(consent_id)


    async def get_consent_by_token(self, token: str) -> ConsentResponse:
        """Retrieve a consent by its unique access token.

        Used for QR code and remote link access.

        Args:
            token: The unique access token.

        Returns:
            The consent as a response DTO.
        """

        consent = await self._consent_repo.find_by_token(token)

        if consent is None:
            raise EntityNotFoundError(f"Consent with token {token} not found")

        return ConsentResponse.model_validate(consent)


    async def list_consents(
        self,
        client_id: UUID | None = None,
        status: ConsentStatus | None = None,
    ) -> list[ConsentResponse]:
        """List consents with optional filters.

        Args:
            client_id: Optional filter by client UUID.
            status: Optional filter by consent status.

        Returns:
            A list of consent response DTOs.
        """

        return await self._list_query.execute(
            client_id=client_id,
            status=status,
        )


    async def sign_consent(
        self,
        consent_id: UUID,
        request: SignConsentRequest,
    ) -> ConsentResponse:
        """Sign a consent document.

        Args:
            consent_id: UUID of the consent to sign.
            request: Validated signing data.

        Returns:
            The signed consent as a response DTO.
        """

        return await self._sign_command.execute(consent_id, request)


    async def revoke_consent(self, consent_id: UUID) -> ConsentResponse:
        """Revoke a signed consent.

        Args:
            consent_id: UUID of the consent to revoke.

        Returns:
            The revoked consent as a response DTO.
        """

        return await self._revoke_command.execute(consent_id)
