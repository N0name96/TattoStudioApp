"""Notification repository interface (Protocol)."""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.notification_entity import Notification
from domain.enums.notification_status import NotificationStatus


@runtime_checkable
class NotificationRepository(Protocol):
    async def get_by_id(self, notification_id: UUID) -> Notification | None: ...
    async def save(self, notification: Notification) -> Notification: ...
    async def list_by_user(self, user_id: UUID, status: NotificationStatus | None = None) -> list[Notification]: ...
    async def list_all(self, status: NotificationStatus | None = None) -> list[Notification]: ...
