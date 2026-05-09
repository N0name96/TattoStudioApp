"""Celery task definitions for background notification sending.

These tasks handle the asynchronous delivery of notifications
through configured channels (email, future: SMS).
"""

import logging

from domain.enums.notification_channel import NotificationChannel

logger = logging.getLogger(__name__)


async def send_notification_task(
    notification_id: str,
    user_email: str,
    channel: str,
    title: str,
    message: str,
) -> bool:
    """Send a notification through the configured channel.

    This is an async task that should be called by Celery or
    any background task runner.

    For now, only EMAIL channel is implemented.
    SMS is deferred as it requires a paid provider.

    Args:
        notification_id: UUID string of the notification.
        user_email: Recipient email address.
        channel: The notification channel (email).
        title: Notification title.
        message: Notification body.

    Returns:
        True if the notification was sent successfully.
    """

    logger.info(
        "Processing notification task",
        extra={
            "extra_data": {
                "notification_id": notification_id,
                "channel": channel,
            }
        },
    )

    if channel == NotificationChannel.EMAIL.value:
        logger.info(
            "Email notification",
            extra={
                "extra_data": {
                    "to": user_email,
                    "subject": title,
                    "notification_id": notification_id,
                }
            },
        )

        # TODO: Integrate with actual email service (SendGrid, SMTP, etc.)
        # For now, log the email content
        logger.info(
            "Email body",
            extra={"extra_data": {"body": message}},
        )

        return True

    logger.warning(
        "Unsupported channel",
        extra={"extra_data": {"channel": channel}},
    )

    return False
