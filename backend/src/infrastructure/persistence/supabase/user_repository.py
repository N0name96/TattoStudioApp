"""Supabase implementation of the UserRepository.

This module provides a Supabase-backed repository for User persistence.
Uses the Supabase Python client for database operations.

Usage:
    from infrastructure.persistence.supabase.user_repository import (
        SupabaseUserRepository,
    )
    repo = SupabaseUserRepository(client)
"""

import logging
from uuid import UUID

from supabase import Client

from domain.entities.user_entity import User
from domain.enums.user_role import UserRole
from infrastructure.persistence.supabase.mappers import map_to_user, map_to_user_dict

logger = logging.getLogger(__name__)

TABLE = "users"


class SupabaseUserRepository:
    """Supabase implementation of the UserRepository.

    Persists User entities to a Supabase (PostgreSQL) database.

    Attributes:
        _client: Supabase client instance.
    """

    def __init__(self, client: Client) -> None:
        """Initialize the repository with a Supabase client.

        Args:
            client: Authenticated Supabase client.
        """

        self._client = client

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique ID.

        Args:
            user_id: The UUID of the user to find.

        Returns:
            The User entity if found, None otherwise.
        """

        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("id", str(user_id))
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return map_to_user(response.data[0])

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The User entity if found, None otherwise.
        """

        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return map_to_user(response.data[0])

    async def save(self, user: User) -> User:
        """Persist a user entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            user: The User entity to persist.

        Returns:
            The persisted User entity.
        """

        data = map_to_user_dict(user)

        response = (
            self._client.table(TABLE)
            .upsert(data, on_conflict="id")
            .execute()
        )

        logger.debug(
            "User saved to Supabase",
            extra={"extra_data": {"user_id": str(user.id)}},
        )

        return map_to_user(response.data[0])

    async def list_all(self, role: UserRole | None = None) -> list[User]:
        """List all users, optionally filtering by role.

        Args:
            role: Optional filter by user role.

        Returns:
            A list of User entities ordered by creation date.
        """

        query = self._client.table(TABLE).select("*").order("created_at")

        if role is not None:
            query = query.eq("role", role.value)

        response = query.execute()

        return [map_to_user(row) for row in response.data]

    async def delete(self, user_id: UUID) -> None:
        """Remove a user by their unique identifier.

        Args:
            user_id: The UUID of the user to delete.
        """

        self._client.table(TABLE).delete().eq("id", str(user_id)).execute()

        logger.debug(
            "User deleted from Supabase",
            extra={"extra_data": {"user_id": str(user_id)}},
        )
