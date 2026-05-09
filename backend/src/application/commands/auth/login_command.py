"""Command to authenticate a user in the TattoStudioApp.

This command handles the login flow:
1. Find user by email
2. Verify password
3. Generate access and refresh tokens
4. Return token response DTO
"""

import logging

from application.dto.requests.auth.login_request import LoginRequest
from application.dto.responses.auth.token_response import TokenResponse
from core.config import settings
from core.errors import UnauthorizedError
from domain.repositories.user_repository import UserRepository
from infrastructure.security.security_service import SecurityService

logger = logging.getLogger(__name__)


class LoginCommand:
    """Command to authenticate a user and issue tokens.

    This command validates credentials, verifies the password hash,
    and generates JWT access and refresh tokens.

    Attributes:
        _user_repo: Repository for user lookups.
        _security_service: Service for password verification and token creation.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        security_service: SecurityService,
    ) -> None:
        """Initialize the command with required dependencies.

        Args:
            user_repo: Repository for user lookups.
            security_service: Service for password verification and token creation.
        """

        self._user_repo = user_repo
        self._security_service = security_service

    async def execute(self, request: LoginRequest) -> TokenResponse:
        """Execute the login flow.

        Steps:
            1. Find user by email.
            2. Verify the password.
            3. Check if user is active.
            4. Generate tokens.
            5. Return the token response DTO.

        Args:
            request: Validated login credentials.

        Returns:
            JWT tokens as a response DTO.

        Raises:
            UnauthorizedError: If email not found or password is wrong.
        """

        logger.info(
            "User login attempt",
            extra={"extra_data": {"email": request.email}},
        )

        # Step 1: Find user by email
        user = await self._user_repo.get_by_email(request.email)

        if user is None:
            raise UnauthorizedError("Invalid email or password")

        # Step 2: Verify the password
        if not self._security_service.verify_password(
            request.password, user.hashed_password
        ):
            raise UnauthorizedError("Invalid email or password")

        # Step 3: Check if user is active
        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        # Step 4: Generate tokens
        access_token = self._security_service.create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        refresh_token = self._security_service.create_refresh_token(
            user_id=user.id,
        )

        logger.info(
            "User logged in successfully",
            extra={"extra_data": {"user_id": str(user.id)}},
        )

        # Step 5: Return token response
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
