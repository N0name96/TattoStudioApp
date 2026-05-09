"""API handler for consent endpoints.

This module provides the FastAPI router for consent operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).

Endpoints:
    POST   /consents              - Create consent (admin)
    GET    /consents/{id}          - Get consent detail
    POST   /consents/{id}/sign     - Sign consent (client)
    POST   /consents/{id}/revoke   - Revoke consent (admin/client)
    GET    /consents               - List consents with filters
    GET    /consents/token/{token} - Get consent by token (public QR/remote)
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.consents.create_consent_request import (
    CreateConsentRequest,
)
from application.dto.requests.consents.sign_consent_request import (
    SignConsentRequest,
)
from application.dto.responses.consents.consent_response import (
    ConsentResponse,
)
from application.use_cases.consents.consent_use_case import (
    ConsentUseCase,
)
from core.container import container
from core.errors import (
    BusinessRuleError,
    EntityNotFoundError,
)
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consents", tags=["consents"])


def get_consent_use_case() -> ConsentUseCase:
    """Dependency injection for the ConsentUseCase.

    Uses the DI container to resolve the repository implementations.

    Returns:
        A ConsentUseCase instance.
    """

    return ConsentUseCase(
        consent_repo=container.consent_repository,
        client_repo=container.client_repository,
    )


@router.post(
    "/",
    response_model=SuccessResponse[ConsentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_consent(
    request: CreateConsentRequest,
    use_case: ConsentUseCase = Depends(get_consent_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ConsentResponse]:
    """Create a new consent document (admin only).

    Generates a unique token that can be shared with the client
    via QR code or remote link for signing.

    Args:
        request: Validated consent creation data.
        use_case: Injected use case for consent operations.
        current_user: The authenticated admin user.

    Returns:
        A success response containing the created consent with token.

    Raises:
        HTTPException: 404 if the client does not exist.
    """

    try:
        consent = await use_case.create_consent(request)

        return SuccessResponse(data=consent, message="Consent created successfully")

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e


@router.get(
    "/token/{token}",
    response_model=SuccessResponse[ConsentResponse],
)
async def get_consent_by_token(
    token: str,
    use_case: ConsentUseCase = Depends(get_consent_use_case),
) -> SuccessResponse[ConsentResponse]:
    """Retrieve a consent by its unique access token (public).

    This endpoint is used when clients scan a QR code or click a link
    to access their consent document. No authentication required.

    Args:
        token: The unique URL-safe access token.
        use_case: Injected use case for consent operations.

    Returns:
        A success response containing the consent data.

    Raises:
        HTTPException: 404 if the consent is not found.
    """

    try:
        consent = await use_case.get_consent_by_token(token)

        return SuccessResponse(data=consent)

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e


@router.get(
    "/{consent_id}",
    response_model=SuccessResponse[ConsentResponse],
)
async def get_consent(
    consent_id: UUID,
    use_case: ConsentUseCase = Depends(get_consent_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[ConsentResponse]:
    """Retrieve a consent by its unique identifier.

    Args:
        consent_id: The UUID of the consent to retrieve.
        use_case: Injected use case for consent operations.
        current_user: The authenticated user.

    Returns:
        A success response containing the consent data.

    Raises:
        HTTPException: 404 if the consent is not found.
    """

    try:
        consent = await use_case.get_consent(consent_id)

        return SuccessResponse(data=consent)

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e


@router.get(
    "/",
    response_model=SuccessResponse[list[ConsentResponse]],
)
async def list_consents(
    client_id: UUID | None = None,
    use_case: ConsentUseCase = Depends(get_consent_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[ConsentResponse]]:
    """List consents with optional filters.

    Args:
        client_id: Optional filter by client UUID.
        use_case: Injected use case for consent operations.
        current_user: The authenticated user.

    Returns:
        A success response containing a list of consents.
    """

    consents = await use_case.list_consents(client_id=client_id)

    return SuccessResponse(data=consents)


@router.post(
    "/{consent_id}/sign",
    response_model=SuccessResponse[ConsentResponse],
)
async def sign_consent(
    consent_id: UUID,
    request: SignConsentRequest,
    use_case: ConsentUseCase = Depends(get_consent_use_case),
) -> SuccessResponse[ConsentResponse]:
    """Sign a consent document (public or authenticated).

    The client provides their signature data (base64 encoded).
    This endpoint can be called from the QR code flow or
    the authenticated client portal.

    Args:
        consent_id: The UUID of the consent to sign.
        request: Validated signing data with signature.
        use_case: Injected use case for consent operations.

    Returns:
        A success response containing the signed consent.

    Raises:
        HTTPException: 404 if the consent is not found.
        HTTPException: 422 if the consent cannot be signed.
    """

    try:
        consent = await use_case.sign_consent(consent_id, request)

        return SuccessResponse(data=consent, message="Consent signed successfully")

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e

    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        ) from e


@router.post(
    "/{consent_id}/revoke",
    response_model=SuccessResponse[ConsentResponse],
)
async def revoke_consent(
    consent_id: UUID,
    use_case: ConsentUseCase = Depends(get_consent_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[ConsentResponse]:
    """Revoke a signed consent (admin only).

    Args:
        consent_id: The UUID of the consent to revoke.
        use_case: Injected use case for consent operations.
        current_user: The authenticated admin user.

    Returns:
        A success response containing the revoked consent.

    Raises:
        HTTPException: 404 if the consent is not found.
        HTTPException: 422 if the consent cannot be revoked.
    """

    try:
        consent = await use_case.revoke_consent(consent_id)

        return SuccessResponse(data=consent, message="Consent revoked successfully")

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e

    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        ) from e
