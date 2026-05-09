"""Response DTO for notification data."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.enums.notification_channel import NotificationChannel
from domain.enums.notification_status import NotificationStatus
from domain.enums.notification_type import NotificationType


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    type: NotificationType
    status: NotificationStatus
    channel: NotificationChannel
    title: str
    message: str
    is_read: bool
    sent_at: datetime | None
    created_at: datetime
    updated_at: datetime
