"""Command to refresh an access token in the TattoStudioApp.

This command handles the token refresh flow:
1. Validate the refresh token
2. Extract user_id from token
3. Fetch user from repository
4. Generate new access token
5. Return token response DTO
"""

import logging

from application.dto.requests.auth.refresh_token_request import RefreshTokenRequest
from application.dto.responses.auth.token_response import TokenResponse
from core.config import settings
from core.errors import EntityNotFoundError, UnauthorizedError
from domain.repositories.user_repository import UserRepository
from infrastructure.security.security_service import SecurityService

logger = logging.getLogger(__name__)


class RefreshTokenCommand:
    """Command to refresh an access token using a refresh token.

    This command validates the refresh token, verifies the user exists,
    and generates a new access token.

    Attributes:
        _user_repo: Repository for user lookups.
        _security_service: Service for token decoding and creation.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        security_service: SecurityService,
    ) -> None:
        """Initialize the command with required dependencies.

        Args:
            user_repo: Repository for user lookups.
            security_service: Service for token decoding and creation.
        """

        self._user_repo = user_repo
        self._security_service = security_service

    async def execute(self, request: RefreshTokenRequest) -> TokenResponse:
        """Execute the token refresh flow.

        Steps:
            1. Decode and validate the refresh token.
            2. Verify token type is "refresh".
            3. Fetch user from repository.
            4. Generate new access token.
            5. Return the token response DTO.

        Args:
            request: Validated refresh token data.

        Returns:
            New JWT tokens as a response DTO.

        Raises:
            UnauthorizedError: If the token is invalid or expired.
            EntityNotFoundError: If the user no longer exists.
        """

        logger.info("Refreshing access token")

        # Step 1: Decode and validate the refresh token
        payload = self._security_service.decode_token(request.refresh_token)

        # Step 2: Verify token type is "refresh"
        token_type = payload.get("type")

        if token_type != "refresh":
            raise UnauthorizedError("Invalid token type")

        # Step 3: Extract user_id and fetch user
        user_id_str = payload.get("sub")

        if user_id_str is None:
            raise UnauthorizedError("Invalid token payload")

        from uuid import UUID

        user_id = UUID(user_id_str)
        user = await self._user_repo.get_by_id(user_id)

        if user is None:
            raise EntityNotFoundError(f"User {user_id} not found")

        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        # Step 4: Generate new access token
        access_token = self._security_service.create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        # Generate new refresh token
        refresh_token = self._security_service.create_refresh_token(
            user_id=user.id,
        )

        logger.info(
            "Access token refreshed successfully",
            extra={"extra_data": {"user_id": str(user.id)}},
        )

        # Step 5: Return token response
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
