"""In-memory notification repository."""

from uuid import UUID
from domain.entities.notification_entity import Notification
from domain.enums.notification_status import NotificationStatus


class InMemoryNotificationRepository:
    def __init__(self) -> None:
        self._storage: dict[UUID, Notification] = {}

    async def get_by_id(self, notification_id: UUID) -> Notification | None:
        return self._storage.get(notification_id)

    async def save(self, notification: Notification) -> Notification:
        self._storage[notification.id] = notification
        return notification

    async def list_by_user(
        self, user_id: UUID, status: NotificationStatus | None = None
    ) -> list[Notification]:
        notifications = [n for n in self._storage.values() if n.user_id == user_id]
        if status is not None:
            notifications = [n for n in notifications if n.status == status]
        return sorted(notifications, key=lambda n: n.created_at, reverse=True)

    async def list_all(
        self, status: NotificationStatus | None = None
    ) -> list[Notification]:
        notifications = list(self._storage.values())
        if status is not None:
            notifications = [n for n in notifications if n.status == status]
        return sorted(notifications, key=lambda n: n.created_at, reverse=True)
