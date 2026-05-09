"""Response DTOs for the appointments module.

Contains Pydantic models for serializing appointment data.
These DTOs are used by the API layer to format responses.
"""

from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


class AppointmentResponse(BaseModel):
    """Response DTO for appointment data.

    Used to return appointment information to the API client.
    Maps from domain entity to a serializable format.

    Attributes:
        id: Unique identifier for the appointment.
        client_id: UUID of the client who booked the appointment.
        artist_id: UUID of the artist performing the service.
        service_type: Type of service being performed.
        date: Date of the appointment.
        start_time: Start time of the appointment.
        end_time: End time of the appointment.
        status: Current status of the appointment.
        notes: Optional notes from the client.
        total_price: Total price for the service.
        created_at: When the appointment was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_id: UUID
    artist_id: UUID
    service_type: ServiceType
    date: date
    start_time: time
    end_time: time
    status: AppointmentStatus
    notes: str | None
    total_price: float
    created_at: datetime
