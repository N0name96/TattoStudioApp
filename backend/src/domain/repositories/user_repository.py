"""User repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any user repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/in_memory/user_repository.py
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.user_entity import User
from domain.enums.user_role import UserRole


@runtime_checkable
class UserRepository(Protocol):
    """Interface for User persistence.

    This protocol defines the contract that any user repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer by the InMemory and Supabase repositories.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: The UUID of the user to find.

        Returns:
            The User entity if found, None otherwise.
        """
        ...

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The User entity if found, None otherwise.
        """
        ...

    async def save(self, user: User) -> User:
        """Persist a user entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            user: The User entity to persist.

        Returns:
            The persisted User entity.
        """
        ...

    async def list_all(self, role: UserRole | None = None) -> list[User]:
        """List all users, optionally filtering by role.

        Args:
            role: Optional filter by user role.

        Returns:
            A list of User entities.
        """
        ...

    async def delete(self, user_id: UUID) -> None:
        """Remove a user by their unique identifier.

        Args:
            user_id: The UUID of the user to delete.
        """
        ...
