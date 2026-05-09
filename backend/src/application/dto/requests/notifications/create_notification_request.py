"""Request DTO for creating a notification."""

from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.notification_channel import NotificationChannel
from domain.enums.notification_type import NotificationType


class CreateNotificationRequest(BaseModel):
    user_id: UUID
    type: NotificationType = NotificationType.OTHER
    channel: NotificationChannel = NotificationChannel.EMAIL
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=2000)
