"""Notification domain entity."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.notification_channel import NotificationChannel
from domain.enums.notification_status import NotificationStatus
from domain.enums.notification_type import NotificationType


VALID_TRANSITIONS: dict[NotificationStatus, list[NotificationStatus]] = {
    NotificationStatus.PENDING: [NotificationStatus.SENT, NotificationStatus.FAILED],
    NotificationStatus.SENT: [],
    NotificationStatus.FAILED: [],
}


@dataclass
class Notification:
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


    @classmethod
    def create(
        cls,
        user_id: UUID,
        type: NotificationType,
        channel: NotificationChannel,
        title: str,
        message: str,
    ) -> "Notification":
        if not title.strip():
            raise BusinessRuleError("Notification title cannot be empty")
        if not message.strip():
            raise BusinessRuleError("Notification message cannot be empty")

        now = datetime.now()

        return cls(
            id=uuid4(),
            user_id=user_id,
            type=type,
            status=NotificationStatus.PENDING,
            channel=channel,
            title=title,
            message=message,
            is_read=False,
            sent_at=None,
            created_at=now,
            updated_at=now,
        )


    def mark_sent(self) -> None:
        if self.status != NotificationStatus.PENDING:
            raise BusinessRuleError("Can only mark PENDING notifications as sent")
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.now()
        self.updated_at = datetime.now()


    def mark_failed(self) -> None:
        if self.status != NotificationStatus.PENDING:
            raise BusinessRuleError("Can only mark PENDING notifications as failed")
        self.status = NotificationStatus.FAILED
        self.updated_at = datetime.now()


    def mark_read(self) -> None:
        self.is_read = True
        self.updated_at = datetime.now()
