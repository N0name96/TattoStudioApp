"""Artist domain entity for the TattoStudioApp.

This module contains the Artist entity with all business logic
for artist profile management and lifecycle operations.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from core.errors import BusinessRuleError


@dataclass
class Artist:
    """Represents a tattoo artist in the system.

    Attributes:
        id: Unique identifier for the artist.
        name: Artist full name.
        specialty: Artist specialty or style.
        email: Contact email for the artist.
        phone: Optional phone number.
        bio: Artist biography or profile description.
        is_active: Whether the artist is currently active.
        created_at: When the artist was created.
        updated_at: When the artist was last updated.
    """

    id: UUID
    name: str
    specialty: str
    email: str
    phone: str | None
    bio: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        name: str,
        specialty: str,
        email: str,
        phone: str | None = None,
        bio: str | None = None,
    ) -> "Artist":
        """Create a new Artist entity with default lifecycle values."""

        now = datetime.now()

        return cls(
            id=uuid4(),
            name=name,
            specialty=specialty,
            email=email,
            phone=phone,
            bio=bio,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def update_profile(
        self,
        name: str | None = None,
        specialty: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        bio: str | None = None,
        is_active: bool | None = None,
    ) -> None:
        """Update artist profile fields.

        Raises:
            BusinessRuleError: If provided values violate business rules.
        """

        if name is not None:
            self.name = name
        if specialty is not None:
            self.specialty = specialty
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if bio is not None:
            self.bio = bio
        if is_active is not None:
            self.is_active = is_active

        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Deactivate the artist."""

        if not self.is_active:
            raise BusinessRuleError("Artist is already inactive")

        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activate the artist."""

        if self.is_active:
            raise BusinessRuleError("Artist is already active")

        self.is_active = True
        self.updated_at = datetime.now()
