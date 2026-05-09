"""Client domain entity for the TattoStudioApp.

This module contains the Client entity with all business logic
for client profile management and lifecycle operations.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.client_source import ClientSource
from domain.enums.image_rights import ImageRights


@dataclass
class Client:
    """Represents a client in the tattoo studio.

    This entity contains core client data including contact info,
    medical conditions, origin source, and image rights preferences.

    Attributes:
        id: Unique identifier for the client.
        full_name: Client's full name.
        email: Contact email address.
        phone: Phone number.
        birth_date: Client's birth date.
        allergies: Known allergies (empty string if none).
        medical_conditions: Known medical conditions (empty string if none).
        source: How the client discovered the studio.
        image_rights: Set of image rights granted by the client.
        notes: Internal notes from the artist or admin.
        is_active: Whether the client record is active.
        created_at: When the client record was created.
        updated_at: When the client record was last updated.
    """

    id: UUID
    full_name: str
    email: str
    phone: str | None
    birth_date: datetime | None
    allergies: str
    medical_conditions: str
    source: ClientSource | None
    image_rights: set[ImageRights]
    notes: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        full_name: str,
        email: str,
        phone: str | None = None,
        birth_date: datetime | None = None,
        allergies: str = "",
        medical_conditions: str = "",
        source: ClientSource | None = None,
        notes: str = "",
    ) -> "Client":
        """Create a new Client entity with default lifecycle values.

        This is the factory method for creating clients.
        All new clients start as active with empty image rights.

        Args:
            full_name: Client's full name.
            email: Contact email address.
            phone: Optional phone number.
            birth_date: Optional birth date.
            allergies: Known allergies (default empty).
            medical_conditions: Known medical conditions (default empty).
            source: How the client discovered the studio.
            notes: Internal notes from the artist or admin.

        Returns:
            A new Client instance with active status.
        """

        now = datetime.now()

        return cls(
            id=uuid4(),
            full_name=full_name,
            email=email,
            phone=phone,
            birth_date=birth_date,
            allergies=allergies,
            medical_conditions=medical_conditions,
            source=source,
            image_rights=set(),
            notes=notes,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def update_profile(
        self,
        full_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        birth_date: datetime | None = None,
        allergies: str | None = None,
        medical_conditions: str | None = None,
        source: ClientSource | None = None,
        notes: str | None = None,
    ) -> None:
        """Update client profile fields.

        Only provided fields are updated. Use None to skip a field.

        Args:
            full_name: New full name.
            email: New contact email.
            phone: New phone number.
            birth_date: New birth date.
            allergies: Updated allergies info.
            medical_conditions: Updated medical conditions info.
            source: Updated source channel.
            notes: Updated internal notes.
        """

        if full_name is not None:
            self.full_name = full_name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if birth_date is not None:
            self.birth_date = birth_date
        if allergies is not None:
            self.allergies = allergies
        if medical_conditions is not None:
            self.medical_conditions = medical_conditions
        if source is not None:
            self.source = source
        if notes is not None:
            self.notes = notes

        self.updated_at = datetime.now()

    def grant_image_rights(self, rights: set[ImageRights]) -> None:
        """Grant specific image rights to the studio.

        Args:
            rights: Set of image rights to grant.
        """

        self.image_rights = rights
        self.updated_at = datetime.now()

    def revoke_image_rights(self) -> None:
        """Revoke all image rights."""

        self.image_rights = set()
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Deactivate the client record.

        Raises:
            BusinessRuleError: If the client is already inactive.
        """

        if not self.is_active:
            raise BusinessRuleError("Client is already inactive")

        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activate the client record.

        Raises:
            BusinessRuleError: If the client is already active.
        """

        if self.is_active:
            raise BusinessRuleError("Client is already active")

        self.is_active = True
        self.updated_at = datetime.now()
