"""In-memory mock implementation of the UserRepository.

This module provides a non-persistent repository for development
and testing purposes. Data is stored in memory and lost on restart.

Usage:
    from infrastructure.persistence.in_memory.user_repository import (
        InMemoryUserRepository,
    )
    repo = InMemoryUserRepository()
"""

import logging
from uuid import UUID

from domain.entities.user_entity import User
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)


class InMemoryUserRepository:
    """In-memory implementation of the UserRepository.

    Stores users in dictionaries for development and testing.
    Data is lost when the application restarts.

    Attributes:
        _storage: Dictionary mapping user IDs to entities.
        _email_index: Dictionary mapping emails to user IDs for O(1) lookup.
    """

    def __init__(self) -> None:
        """Initialize the in-memory storage."""

        self._storage: dict[UUID, User] = {}
        self._email_index: dict[str, UUID] = {}

        logger.info("InMemoryUserRepository initialized")

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique ID.

        Args:
            user_id: The UUID of the user to find.

        Returns:
            The User entity if found, None otherwise.
        """

        return self._storage.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Uses the email index for O(1) lookup performance.

        Args:
            email: The email address to search for.

        Returns:
            The User entity if found, None otherwise.
        """

        user_id = self._email_index.get(email)

        if user_id is None:
            return None

        return self._storage.get(user_id)

    async def save(self, user: User) -> User:
        """Persist a user entity (create or update).

        Updates the email index when a new email is added.

        Args:
            user: The User entity to persist.

        Returns:
            The persisted User entity.
        """

        self._storage[user.id] = user
        self._email_index[user.email] = user.id

        logger.debug(
            "User saved",
            extra={"extra_data": {"user_id": str(user.id)}},
        )

        return user

    async def list_all(self, role: UserRole | None = None) -> list[User]:
        """List all users, optionally filtering by role.

        Args:
            role: Optional filter by user role.

        Returns:
            A list of User entities.
        """

        results = list(self._storage.values())

        if role is not None:
            results = [u for u in results if u.role == role]

        return sorted(results, key=lambda u: u.created_at)

    async def delete(self, user_id: UUID) -> None:
        """Remove a user by their unique identifier.

        Also removes the email index entry.

        Args:
            user_id: The UUID of the user to delete.
        """

        user = self._storage.pop(user_id, None)

        if user is not None:
            self._email_index.pop(user.email, None)
