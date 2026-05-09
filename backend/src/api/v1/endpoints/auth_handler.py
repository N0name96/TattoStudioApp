"""API handler for authentication endpoints.

This module provides the FastAPI router for auth operations.
Handlers only orchestrate: receive request, call use case, return response.

All business logic is in the Application layer (commands/queries/use_cases).
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user
from application.dto.requests.auth.login_request import LoginRequest
from application.dto.requests.auth.refresh_token_request import RefreshTokenRequest
from application.dto.requests.auth.register_request import RegisterRequest
from application.dto.responses.auth.token_response import TokenResponse
from application.dto.responses.auth.user_response import UserResponse
from application.use_cases.auth.auth_use_case import AuthUseCase
from core.container import container
from core.errors import (
    DuplicateEntityError,
    EntityNotFoundError,
    UnauthorizedError,
)
from core.responses import SuccessResponse
from domain.entities.user_entity import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_use_case() -> AuthUseCase:
    """Dependency injection for the AuthUseCase.

    Uses the global container for repository and security dependencies.

    Returns:
        An AuthUseCase instance.
    """

    return AuthUseCase(
        user_repo=container.user_repository,
        security_service=container.security_service,
    )


@router.post(
    "/register",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> SuccessResponse[UserResponse]:
    """Register a new user account.

    Creates a new user with the provided data. The email must be unique.

    Args:
        request: Validated registration data.
        use_case: Injected use case for auth operations.

    Returns:
        A success response containing the created user data.

    Raises:
        HTTPException: 409 if the email is already registered.
    """

    try:
        user = await use_case.register(request)

        return SuccessResponse(
            data=user,
            message="User registered successfully",
        )
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.post(
    "/login",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginRequest,
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> SuccessResponse[TokenResponse]:
    """Authenticate a user and issue JWT tokens.

    Validates the email and password, then returns access and refresh tokens.

    Args:
        request: Validated login credentials.
        use_case: Injected use case for auth operations.

    Returns:
        A success response containing JWT tokens.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """

    try:
        tokens = await use_case.login(request)

        return SuccessResponse(
            data=tokens,
            message="Login successful",
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/refresh",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> SuccessResponse[TokenResponse]:
    """Refresh an access token using a refresh token.

    Validates the refresh token and issues new access and refresh tokens.

    Args:
        request: Validated refresh token data.
        use_case: Injected use case for auth operations.

    Returns:
        A success response containing new JWT tokens.

    Raises:
        HTTPException: 401 if the refresh token is invalid.
    """

    try:
        tokens = await use_case.refresh_token(request)

        return SuccessResponse(
            data=tokens,
            message="Token refreshed successfully",
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


@router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[UserResponse]:
    """Get the current authenticated user's profile.

    Requires a valid JWT access token in the Authorization header.

    Args:
        current_user: The authenticated user from the dependency.

    Returns:
        A success response containing the user's profile data.
    """

    user_response = UserResponse.model_validate(current_user)

    return SuccessResponse(data=user_response)
