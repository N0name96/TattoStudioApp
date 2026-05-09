"""Dependency injection for the TattoStudioApp API layer.

This module provides FastAPI dependencies for authentication,
authorization, and use case injection.

Usage:
    from api.deps import get_current_user, require_role
"""

import logging
from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.container import container
from core.errors import UnauthorizedError
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole
from domain.repositories.user_repository import UserRepository
from infrastructure.security.security_service import SecurityService

logger = logging.getLogger(__name__)

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_security_service() -> SecurityService:
    """Dependency that provides the SecurityService instance.

    Returns:
        A singleton SecurityService instance for JWT operations.
    """

    return container.security_service


def get_user_repository() -> UserRepository:
    """Dependency that provides the UserRepository instance.

    Returns:
        A singleton UserRepository implementation.
    """

    return container.user_repository


def get_user_repository_singleton() -> UserRepository:
    """Dependency that provides a singleton UserRepository instance.

    Returns:
        A singleton UserRepository implementation.
    """

    return container.user_repository


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository_singleton),
    security_service: SecurityService = Depends(get_security_service),
) -> User:
    """Extract and validate the current user from the JWT token.

    This dependency decodes the JWT token, fetches the user from
    the repository, and returns the User entity.

    Args:
        token: JWT token from the Authorization header.
        user_repo: Repository for user lookups.
        security_service: Service for token decoding.

    Returns:
        The authenticated User entity.

    Raises:
        HTTPException: 401 if token is invalid or user not found.
    """

    try:
        # Decode the token
        payload = security_service.decode_token(token)

        # Verify token type is "access"
        token_type = payload.get("type")

        if token_type != "access":
            raise UnauthorizedError("Invalid token type")

        # Extract user_id
        user_id_str = payload.get("sub")

        if user_id_str is None:
            raise UnauthorizedError("Invalid token payload")

        from uuid import UUID

        user_id = UUID(user_id_str)

        # Fetch user from repository
        user = await user_repo.get_by_id(user_id)

        if user is None:
            raise UnauthorizedError("User not found")

        return user

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        logger.warning(
            "Authentication failed",
            extra={"extra_data": {"error": str(e)}},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Verify that the current user is active.

    This dependency checks that the user account is not deactivated.

    Args:
        current_user: The authenticated user from get_current_user.

    Returns:
        The active User entity.

    Raises:
        HTTPException: 403 if the user account is inactive.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return current_user


def require_role(*roles: UserRole) -> Callable:
    """Factory dependency that checks if the user has one of the required roles.

    Args:
        *roles: One or more UserRole values that are allowed.

    Returns:
        A FastAPI dependency function that checks the user's role.
    """

    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        """Check if the current user has one of the required roles.

        Args:
            current_user: The active user from get_current_active_user.

        Returns:
            The User entity if role check passes.

        Raises:
            HTTPException: 403 if the user doesn't have the required role.
        """

        if current_user.role not in roles:
            allowed_roles = ", ".join(r.value for r in roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {allowed_roles}",
            )

        return current_user

    return role_checker
