"""Command to create a notification."""

import logging
from application.dto.requests.notifications.create_notification_request import (
    CreateNotificationRequest,
)
from application.dto.responses.notifications.notification_response import (
    NotificationResponse,
)
from core.errors import EntityNotFoundError
from domain.entities.notification_entity import Notification
from domain.repositories.notification_repository import NotificationRepository
from domain.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class CreateNotificationCommand:
    def __init__(
        self,
        notification_repo: NotificationRepository,
        user_repo: UserRepository,
    ) -> None:
        self._notification_repo = notification_repo
        self._user_repo = user_repo

    async def execute(self, request: CreateNotificationRequest) -> NotificationResponse:
        user = await self._user_repo.get_by_id(request.user_id)
        if user is None:
            raise EntityNotFoundError(f"User {request.user_id} not found")

        notification = Notification.create(
            user_id=request.user_id,
            type=request.type,
            channel=request.channel,
            title=request.title,
            message=request.message,
        )

        saved = await self._notification_repo.save(notification)

        logger.info(
            "Notification created",
            extra={"extra_data": {"notification_id": str(saved.id), "type": saved.type.value}},
        )

        return NotificationResponse.model_validate(saved)
