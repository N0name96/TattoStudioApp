"""Query to retrieve the current authenticated user.

This query handles the read operation for user data,
mapping from domain entity to response DTO.
"""

import logging
from uuid import UUID

from application.dto.responses.auth.user_response import UserResponse
from core.errors import EntityNotFoundError
from domain.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class GetCurrentUserQuery:
    """Query to retrieve the current authenticated user by ID.

    This query handles the read operation for user data,
    mapping from domain entity to response DTO.

    Attributes:
        _user_repo: Repository for user lookups.
    """

    def __init__(self, user_repo: UserRepository) -> None:
        """Initialize the query with the user repository.

        Args:
            user_repo: Repository for user lookups.
        """

        self._user_repo = user_repo

    async def execute(self, user_id: UUID) -> UserResponse:
        """Execute the user retrieval.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The user data as a response DTO.

        Raises:
            EntityNotFoundError: If the user does not exist.
        """

        logger.debug(
            "Retrieving current user",
            extra={"extra_data": {"user_id": str(user_id)}},
        )

        user = await self._user_repo.get_by_id(user_id)

        if user is None:
            raise EntityNotFoundError(f"User {user_id} not found")

        return UserResponse.model_validate(user)
