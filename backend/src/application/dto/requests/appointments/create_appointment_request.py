"""Request DTOs for the appointments module.

Contains Pydantic models for validating incoming appointment data.
These DTOs are used by the API layer and commands to validate input.
"""

from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.service_type import ServiceType


class CreateAppointmentRequest(BaseModel):
    """Request DTO for creating a new appointment.

    Contains all the data needed to schedule an appointment
    between a client and an artist.

    Attributes:
        artist_id: UUID of the artist performing the service.
        service_type: Type of service being requested.
        date: Date of the appointment (must be today or future).
        start_time: Start time of the appointment.
        notes: Optional notes from the client about the service.
    """

    artist_id: UUID
    service_type: ServiceType
    date: date
    start_time: time
    notes: str | None = Field(default=None, max_length=500)
