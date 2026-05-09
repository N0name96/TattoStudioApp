"""Appointment status enumeration for the TattoStudioApp.

Defines all possible states of an appointment and valid transitions.
Used to track the lifecycle of an appointment from creation to completion.

Valid transitions:
    PENDING -> CONFIRMED (accept)
    PENDING -> CANCELLED (reject)
    CONFIRMED -> IN_PROGRESS (start)
    CONFIRMED -> CANCELLED (cancel)
    IN_PROGRESS -> COMPLETED (complete)
    IN_PROGRESS -> NO_SHOW (no_show)
"""

from enum import Enum


class AppointmentStatus(str, Enum):
    """Represents the possible states of an appointment.

    Uses str mixin for easy JSON serialization without custom encoders.

    Attributes:
        PENDING: Waiting for artist confirmation.
        CONFIRMED: Accepted by the artist.
        IN_PROGRESS: Service is currently being delivered.
        COMPLETED: Service finished successfully.
        CANCELLED: Appointment was cancelled (by client or artist).
        NO_SHOW: Client did not show up for the appointment.
    """

    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
