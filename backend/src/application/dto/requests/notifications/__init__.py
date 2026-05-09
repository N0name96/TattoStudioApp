"""DTO init."""

from application.dto.requests.notifications.create_notification_request import (
    CreateNotificationRequest,
)
from application.dto.responses.notifications.notification_response import (
    NotificationResponse,
)

__all__ = ["CreateNotificationRequest", "NotificationResponse"]
