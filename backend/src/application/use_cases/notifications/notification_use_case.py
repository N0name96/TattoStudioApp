"""Use case for notification operations."""

from uuid import UUID
from application.commands.notifications.create_notification_command import CreateNotificationCommand
from application.commands.notifications.send_notification_command import SendNotificationCommand
from application.dto.requests.notifications.create_notification_request import CreateNotificationRequest
from application.dto.responses.notifications.notification_response import NotificationResponse
from application.queries.notifications.get_notification_query import GetNotificationQuery
from application.queries.notifications.list_notifications_query import ListNotificationsQuery
from domain.repositories.notification_repository import NotificationRepository
from domain.repositories.user_repository import UserRepository


class NotificationUseCase:
    def __init__(
        self,
        notification_repo: NotificationRepository,
        user_repo: UserRepository,
    ) -> None:
        self._notification_repo = notification_repo
        self._create_command = CreateNotificationCommand(notification_repo, user_repo)
        self._send_command = SendNotificationCommand(notification_repo)
        self._get_query = GetNotificationQuery(notification_repo)
        self._list_query = ListNotificationsQuery(notification_repo)

    async def create_notification(self, request: CreateNotificationRequest) -> NotificationResponse:
        return await self._create_command.execute(request)

    async def get_notification(self, notification_id: UUID) -> NotificationResponse:
        return await self._get_query.execute(notification_id)

    async def list_notifications(
        self, user_id: UUID | None = None
    ) -> list[NotificationResponse]:
        return await self._list_query.execute(user_id=user_id)

    async def mark_sent(self, notification_id: UUID) -> NotificationResponse:
        return await self._send_command.mark_sent(notification_id)

    async def mark_failed(self, notification_id: UUID) -> NotificationResponse:
        return await self._send_command.mark_failed(notification_id)

    async def mark_read(self, notification_id: UUID) -> NotificationResponse:
        notification = await self._notification_repo.get_by_id(notification_id)
        if notification is None:
            from core.errors import EntityNotFoundError
            raise EntityNotFoundError(f"Notification {notification_id} not found")
        notification.mark_read()
        saved = await self._notification_repo.save(notification)
        return NotificationResponse.model_validate(saved)

    async def mark_all_read(self, user_id: UUID) -> list[NotificationResponse]:
        notifications = await self._notification_repo.list_by_user(user_id)
        for n in notifications:
            if not n.is_read:
                n.mark_read()
                await self._notification_repo.save(n)
        return [NotificationResponse.model_validate(n) for n in notifications]
