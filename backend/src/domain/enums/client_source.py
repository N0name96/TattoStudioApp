"""Client source enumeration for the TattoStudioApp.

This module defines the possible channels through which
clients discover the studio.
"""

from enum import Enum


class ClientSource(str, Enum):
    """Possible sources through which a client discovered the studio.

    Uses str mixin for easy JSON serialization.

    Attributes:
        INSTAGRAM: Found through Instagram.
        TIKTOK: Found through TikTok.
        RECOMMENDATION: Recommended by a friend.
        GOOGLE_MAPS: Found via Google Maps or reviews.
        WALK_IN: Passed by and walked in.
        FAIR_EVENT: Met at a fair or convention.
        OTHER: Other unspecified source.
    """

    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    RECOMMENDATION = "recommendation"
    GOOGLE_MAPS = "google_maps"
    WALK_IN = "walk_in"
    FAIR_EVENT = "fair_event"
    OTHER = "other"
