"""Tests for the Notification domain entity."""

from uuid import uuid4

import pytest

from core.errors import BusinessRuleError
from domain.entities.notification_entity import Notification
from domain.enums.notification_channel import NotificationChannel
from domain.enums.notification_status import NotificationStatus
from domain.enums.notification_type import NotificationType


class TestNotificationCreation:
    def test_create_valid_notification(self):
        n = Notification.create(
            user_id=uuid4(),
            type=NotificationType.APPOINTMENT_REMINDER,
            channel=NotificationChannel.EMAIL,
            title="Recordatorio",
            message="Tu cita es mañana",
        )
        assert n.status == NotificationStatus.PENDING
        assert n.is_read is False
        assert n.sent_at is None

    def test_create_with_empty_title_raises_error(self):
        with pytest.raises(BusinessRuleError, match="title cannot be empty"):
            Notification.create(
                user_id=uuid4(),
                type=NotificationType.OTHER,
                channel=NotificationChannel.EMAIL,
                title="   ",
                message="Body",
            )

    def test_create_with_empty_message_raises_error(self):
        with pytest.raises(BusinessRuleError, match="message cannot be empty"):
            Notification.create(
                user_id=uuid4(),
                type=NotificationType.OTHER,
                channel=NotificationChannel.EMAIL,
                title="Title",
                message="",
            )


class TestNotificationTransitions:
    def test_mark_sent(self):
        n = Notification.create(
            user_id=uuid4(),
            type=NotificationType.POST_CARE,
            channel=NotificationChannel.EMAIL,
            title="Cuidados",
            message="Cuida tu tatuaje",
        )
        n.mark_sent()
        assert n.status == NotificationStatus.SENT
        assert n.sent_at is not None

    def test_mark_failed(self):
        n = Notification.create(
            user_id=uuid4(),
            type=NotificationType.POST_CARE,
            channel=NotificationChannel.EMAIL,
            title="Cuidados",
            message="Cuida tu tatuaje",
        )
        n.mark_failed()
        assert n.status == NotificationStatus.FAILED

    def test_mark_read(self):
        n = Notification.create(
            user_id=uuid4(),
            type=NotificationType.BIRTHDAY,
            channel=NotificationChannel.EMAIL,
            title="Feliz cumple",
            message="Feliz cumpleaños",
        )
        n.mark_read()
        assert n.is_read is True

    def test_cannot_mark_sent_twice(self):
        n = Notification.create(
            user_id=uuid4(),
            type=NotificationType.APPOINTMENT_REMINDER,
            channel=NotificationChannel.EMAIL,
            title="Test",
            message="Test",
        )
        n.mark_sent()
        with pytest.raises(BusinessRuleError):
            n.mark_sent()
