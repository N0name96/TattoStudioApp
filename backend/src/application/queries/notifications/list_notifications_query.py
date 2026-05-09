"""Query to list notifications."""

from uuid import UUID
from application.dto.responses.notifications.notification_response import NotificationResponse
from domain.enums.notification_status import NotificationStatus
from domain.repositories.notification_repository import NotificationRepository


class ListNotificationsQuery:
    def __init__(self, notification_repo: NotificationRepository) -> None:
        self._notification_repo = notification_repo

    async def execute(
        self,
        user_id: UUID | None = None,
        status: NotificationStatus | None = None,
    ) -> list[NotificationResponse]:
        if user_id is not None:
            notifications = await self._notification_repo.list_by_user(user_id, status=status)
        else:
            notifications = await self._notification_repo.list_all(status=status)
        return [NotificationResponse.model_validate(n) for n in notifications]
