"""Use case for authentication operations in the TattoStudioApp.

This module provides a high-level interface for auth operations,
orchestrating commands and queries. It acts as the entry point for
the API layer to interact with the authentication domain.
"""

from uuid import UUID

from application.commands.auth.login_command import LoginCommand
from application.commands.auth.refresh_token_command import RefreshTokenCommand
from application.commands.auth.register_command import RegisterCommand
from application.dto.requests.auth.login_request import LoginRequest
from application.dto.requests.auth.refresh_token_request import RefreshTokenRequest
from application.dto.requests.auth.register_request import RegisterRequest
from application.dto.responses.auth.token_response import TokenResponse
from application.dto.responses.auth.user_response import UserResponse
from application.queries.auth.get_current_user_query import GetCurrentUserQuery
from domain.repositories.user_repository import UserRepository
from infrastructure.security.security_service import SecurityService


class AuthUseCase:
    """Use case for authentication operations.

    Orchestrates commands and queries for the auth module.
    Provides a single entry point for the API layer.

    Attributes:
        _user_repo: Repository for user persistence.
        _security_service: Service for password hashing and JWT operations.
        _register_command: Command for user registration.
        _login_command: Command for user login.
        _refresh_token_command: Command for token refresh.
        _get_current_user_query: Query for retrieving current user.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        security_service: SecurityService,
    ) -> None:
        """Initialize the use case with required dependencies.

        Args:
            user_repo: Repository for user persistence.
            security_service: Service for password hashing and JWT operations.
        """

        self._user_repo = user_repo
        self._security_service = security_service
        self._register_command = RegisterCommand(user_repo, security_service)
        self._login_command = LoginCommand(user_repo, security_service)
        self._refresh_token_command = RefreshTokenCommand(user_repo, security_service)
        self._get_current_user_query = GetCurrentUserQuery(user_repo)

    async def register(self, request: RegisterRequest) -> UserResponse:
        """Register a new user.

        Args:
            request: Validated registration data.

        Returns:
            The created user as a response DTO.
        """

        return await self._register_command.execute(request)

    async def login(self, request: LoginRequest) -> TokenResponse:
        """Authenticate a user and issue tokens.

        Args:
            request: Validated login credentials.

        Returns:
            JWT tokens as a response DTO.
        """

        return await self._login_command.execute(request)

    async def refresh_token(self, request: RefreshTokenRequest) -> TokenResponse:
        """Refresh an access token using a refresh token.

        Args:
            request: Validated refresh token data.

        Returns:
            New JWT tokens as a response DTO.
        """

        return await self._refresh_token_command.execute(request)

    async def get_current_user(self, user_id: UUID) -> UserResponse:
        """Retrieve the current authenticated user.

        Args:
            user_id: UUID of the authenticated user.

        Returns:
            The user data as a response DTO.
        """

        return await self._get_current_user_query.execute(user_id)
