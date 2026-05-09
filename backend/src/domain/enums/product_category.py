"""Product category enumeration for the TattoStudioApp."""

from enum import Enum


class ProductCategory(str, Enum):
    CREAM = "cream"
    INK = "ink"
    NEEDLE = "needle"
    JEWELRY = "jewelry"
    MERCHANDISE = "merchandise"
    OTHER = "other"
