"""Service type enumeration for the TattoStudioApp.

Defines all the types of services offered by the studio.
Used in appointments to categorize the requested service.
"""

from enum import Enum


class ServiceType(str, Enum):
    """Types of services offered by the tattoo studio.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        TATTOO: Traditional tattoo service.
        PIERCING: Body piercing service.
        MICROPIGMENTATION: Micropigmentation (permanent makeup, etc.).
        LASER: Laser tattoo removal or treatment.
        DENTAL_GEMS: Dental gem application.
    """

    TATTOO = "tattoo"
    PIERCING = "piercing"
    MICROPIGMENTATION = "micropigmentation"
    LASER = "laser"
    DENTAL_GEMS = "dental_gems"
