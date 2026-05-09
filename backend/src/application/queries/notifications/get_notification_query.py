"""Query to get a notification by ID."""

from uuid import UUID
from application.dto.responses.notifications.notification_response import NotificationResponse
from core.errors import EntityNotFoundError
from domain.repositories.notification_repository import NotificationRepository


class GetNotificationQuery:
    def __init__(self, notification_repo: NotificationRepository) -> None:
        self._notification_repo = notification_repo

    async def execute(self, notification_id: UUID) -> NotificationResponse:
        notification = await self._notification_repo.get_by_id(notification_id)
        if notification is None:
            raise EntityNotFoundError(f"Notification {notification_id} not found")
        return NotificationResponse.model_validate(notification)
