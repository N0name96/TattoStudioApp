"""Image rights enumeration for the TattoStudioApp.

This module defines the usage permissions a client grants
for photos of their tattoo work.
"""

from enum import Enum


class ImageRights(str, Enum):
    """Image rights granted by the client for their tattoo photos.

    Uses str mixin for easy JSON serialization.

    Attributes:
        SOCIAL_MEDIA: Usage allowed on social media platforms.
        PORTFOLIO: Usage allowed in the artist's online portfolio.
        ADVERTISING: Usage allowed in paid advertising.
    """

    SOCIAL_MEDIA = "social_media"
    PORTFOLIO = "portfolio"
    ADVERTISING = "advertising"
