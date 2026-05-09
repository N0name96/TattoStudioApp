"""Consent type enumeration for the TattoStudioApp.

Defines all the types of consent documents available in the system.
Each type corresponds to a service category with its own legal requirements
and document template.
"""

from enum import Enum


class ConsentType(str, Enum):
    """Types of consent documents offered by the studio.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        TATTOO: Consent for tattoo services.
        PIERCING: Consent for body piercing services.
        MICROPIGMENTATION: Consent for micropigmentation (permanent makeup).
        LASER: Consent for laser tattoo removal or treatment.
        DENTAL_GEMS: Consent for dental gem application.
    """

    TATTOO = "tattoo"
    PIERCING = "piercing"
    MICROPIGMENTATION = "micropigmentation"
    LASER = "laser"
    DENTAL_GEMS = "dental_gems"
