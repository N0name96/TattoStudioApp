"""Notification type enumeration for the TattoStudioApp."""

from enum import Enum


class NotificationType(str, Enum):
    APPOINTMENT_REMINDER = "appointment_reminder"
    POST_CARE = "post_care"
    BIRTHDAY = "birthday"
    PROMOTION = "promotion"
    OTHER = "other"
