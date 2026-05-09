"""Request DTO for updating appointment details.

Contains Pydantic models for validating incoming update data.
All fields are optional to support partial updates.
"""

from datetime import date as date_type
from datetime import time as time_type

from pydantic import BaseModel, Field


class UpdateAppointmentDetailsRequest(BaseModel):
    """Request DTO for updating appointment details.

    All fields are optional. Only provided fields will be updated.

    Attributes:
        date: New date for the appointment.
        start_time: New start time for the appointment.
        notes: New notes (max 500 chars).
        total_price: New price (must be >= 0).
    """

    date: date_type | None = None
    start_time: time_type | None = None
    notes: str | None = Field(default=None, max_length=500)
    total_price: float | None = Field(default=None, ge=0.0)
