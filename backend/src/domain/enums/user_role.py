"""User role enumeration for the TattoStudioApp.

Defines all possible roles a user can have in the system.
Used for authorization and access control across the application.
"""

from enum import Enum


class UserRole(str, Enum):
    """Represents the possible roles for a user.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        CLIENT: Regular customer who books appointments.
        ARTIST: Tattoo artist who provides services.
        ADMIN: Studio administrator with full access.
    """

    CLIENT = "client"
    ARTIST = "artist"
    ADMIN = "admin"
