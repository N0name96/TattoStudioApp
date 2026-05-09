"""User domain entity for the TattoStudioApp.

This module contains the User entity with all business logic
for user lifecycle management including activation, deactivation,
and profile updates.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.user_role import UserRole


@dataclass
class User:
    """Represents a user in the tattoo studio system.

    This entity contains the core business logic for user
    management including activation/deactivation and profile updates.

    Attributes:
        id: Unique identifier for the user.
        email: User's email address (unique).
        hashed_password: PBKDF2-SHA256 hashed password.
        full_name: User's full name.
        role: User's role in the system (client, artist, admin).
        phone: Optional phone number.
        is_active: Whether the user account is active.
        created_at: When the user was created.
        updated_at: When the user was last updated.
    """

    id: UUID
    email: str
    hashed_password: str
    full_name: str
    role: UserRole
    phone: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        email: str,
        hashed_password: str,
        full_name: str,
        role: UserRole = UserRole.CLIENT,
        phone: str | None = None,
    ) -> "User":
        """Create a new user with default settings.

        This is the factory method for creating users. It sets
        default values for is_active and timestamps.

        Args:
            email: User's email address.
            hashed_password: PBKDF2-SHA256 hashed password.
            full_name: User's full name.
            role: User's role (default: CLIENT).
            phone: Optional phone number.

        Returns:
            A new User instance with is_active=True.
        """

        now = datetime.now()

        return cls(
            id=uuid4(),
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            phone=phone,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def deactivate(self) -> None:
        """Deactivate the user account.

        Prevents the user from logging in or accessing the system.

        Raises:
            BusinessRuleError: If the user is already inactive.
        """

        if not self.is_active:
            raise BusinessRuleError("User is already inactive")

        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activate the user account.

        Restores the user's access to the system.

        Raises:
            BusinessRuleError: If the user is already active.
        """

        if self.is_active:
            raise BusinessRuleError("User is already active")

        self.is_active = True
        self.updated_at = datetime.now()

    def update_profile(
        self,
        full_name: str | None = None,
        phone: str | None = None,
    ) -> None:
        """Update mutable user profile details.

        Only provided fields (non-None) are updated.

        Args:
            full_name: New full name (None = don't change).
            phone: New phone number (None = don't change).
        """

        if full_name is not None:
            self.full_name = full_name

        if phone is not None:
            self.phone = phone

        self.updated_at = datetime.now()

    def is_admin(self) -> bool:
        """Check if the user has admin role.

        Returns:
            True if the user is an admin, False otherwise.
        """

        return self.role == UserRole.ADMIN

    def is_artist(self) -> bool:
        """Check if the user has artist role.

        Returns:
            True if the user is an artist, False otherwise.
        """

        return self.role == UserRole.ARTIST

    def is_client(self) -> bool:
        """Check if the user has client role.

        Returns:
            True if the user is a client, False otherwise.
        """

        return self.role == UserRole.CLIENT
