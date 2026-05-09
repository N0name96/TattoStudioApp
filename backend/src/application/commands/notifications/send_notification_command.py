"""Command to send a notification (mark as sent/failed)."""

import logging
from uuid import UUID
from application.dto.responses.notifications.notification_response import (
    NotificationResponse,
)
from core.errors import EntityNotFoundError
from domain.repositories.notification_repository import NotificationRepository

logger = logging.getLogger(__name__)


class SendNotificationCommand:
    def __init__(self, notification_repo: NotificationRepository) -> None:
        self._notification_repo = notification_repo

    async def mark_sent(self, notification_id: UUID) -> NotificationResponse:
        notification = await self._notification_repo.get_by_id(notification_id)
        if notification is None:
            raise EntityNotFoundError(f"Notification {notification_id} not found")

        notification.mark_sent()
        saved = await self._notification_repo.save(notification)
        return NotificationResponse.model_validate(saved)

    async def mark_failed(self, notification_id: UUID) -> NotificationResponse:
        notification = await self._notification_repo.get_by_id(notification_id)
        if notification is None:
            raise EntityNotFoundError(f"Notification {notification_id} not found")

        notification.mark_failed()
        saved = await self._notification_repo.save(notification)
        return NotificationResponse.model_validate(saved)
