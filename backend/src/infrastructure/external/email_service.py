"""Email service protocol for sending notification emails.

For now, only email is supported. SMS is skipped as it is not free.
The actual implementation will use SendGrid or SMTP.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmailServiceProtocol(Protocol):
    """Interface for sending emails.

    Currently only email channel is supported. SMS implementation
    is deferred as it requires a paid provider.
    """

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> bool:
        """Send an email notification.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            body: Email body content (plain text or HTML).

        Returns:
            True if the email was sent successfully.
        """
        ...
