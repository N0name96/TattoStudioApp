"""Google Calendar service protocol for appointment synchronization.

Defines the contract for syncing appointments with Google Calendar.
The actual implementation will use the Google Calendar API.
"""

from datetime import date, time
from typing import Protocol, runtime_checkable


@runtime_checkable
class GoogleCalendarServiceProtocol(Protocol):
    """Interface for Google Calendar integration."""

    async def sync_appointment(
        self,
        artist_email: str,
        appointment_id: str,
        title: str,
        appointment_date: date,
        start_time: time,
        end_time: time,
        notes: str | None = None,
    ) -> str | None:
        """Sync an appointment to the artist's Google Calendar.

        Args:
            artist_email: The artist's Google account email.
            appointment_id: The UUID of the appointment.
            title: Event title.
            appointment_date: Date of the appointment.
            start_time: Start time.
            end_time: End time.
            notes: Optional notes.

        Returns:
            The Google Calendar event ID if successful, None otherwise.
        """
        ...


    async def delete_event(self, artist_email: str, event_id: str) -> bool:
        """Delete a synced event from Google Calendar.

        Args:
            artist_email: The artist's Google account email.
            event_id: The Google Calendar event ID.

        Returns:
            True if deleted successfully.
        """
        ...
