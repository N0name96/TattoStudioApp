"""Appointment domain entity for the TattoStudioApp.

This module contains the Appointment entity with all business logic
for appointment lifecycle management including state transitions
and validation rules.

The entity is framework-agnostic and has no dependencies on
infrastructure or application layers.
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from uuid import UUID, uuid4

from core.errors import BusinessRuleError
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType

# Duration in minutes for each service type
SERVICE_DURATIONS: dict[ServiceType, int] = {
    ServiceType.TATTOO: 120,
    ServiceType.PIERCING: 30,
    ServiceType.MICROPIGMENTATION: 90,
    ServiceType.LASER: 60,
    ServiceType.DENTAL_GEMS: 45,
}

# Valid state transitions
VALID_TRANSITIONS: dict[AppointmentStatus, list[AppointmentStatus]] = {
    AppointmentStatus.PENDING: [
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.CANCELLED,
    ],
    AppointmentStatus.CONFIRMED: [
        AppointmentStatus.IN_PROGRESS,
        AppointmentStatus.CANCELLED,
    ],
    AppointmentStatus.IN_PROGRESS: [
        AppointmentStatus.COMPLETED,
        AppointmentStatus.NO_SHOW,
    ],
    AppointmentStatus.COMPLETED: [],
    AppointmentStatus.CANCELLED: [],
    AppointmentStatus.NO_SHOW: [],
}


@dataclass
class Appointment:
    """Represents an appointment between a client and an artist.

    This entity contains the core business logic for appointment
    lifecycle management including state transitions and validation.

    Attributes:
        id: Unique identifier for the appointment.
        client_id: UUID of the client who booked the appointment.
        artist_id: UUID of the artist performing the service.
        service_type: Type of service being performed.
        date: Date of the appointment.
        start_time: Start time of the appointment.
        end_time: End time of the appointment (calculated from service type).
        status: Current status of the appointment.
        notes: Optional notes from the client.
        total_price: Total price for the service.
        created_at: When the appointment was created.
        updated_at: When the appointment was last updated.
    """

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
    updated_at: datetime

    @classmethod
    def create(
        cls,
        client_id: UUID,
        artist_id: UUID,
        service_type: ServiceType,
        appointment_date: date,
        start_time: time,
        notes: str | None = None,
        total_price: float = 0.0,
    ) -> "Appointment":
        """Create a new appointment with PENDING status.

        This is the factory method for creating appointments. It calculates
        the end_time based on the service type duration.

        Args:
            client_id: UUID of the client booking the appointment.
            artist_id: UUID of the artist performing the service.
            service_type: Type of service being requested.
            appointment_date: Date of the appointment.
            start_time: Start time of the appointment.
            notes: Optional notes from the client.
            total_price: Total price for the service (default 0.0).

        Returns:
            A new Appointment instance with PENDING status.
        """

        # Calculate end_time based on service duration
        duration_minutes = SERVICE_DURATIONS.get(service_type, 60)
        start_datetime = datetime.combine(appointment_date, start_time)
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        end_time = end_datetime.time()

        now = datetime.now()

        return cls(
            id=uuid4(),
            client_id=client_id,
            artist_id=artist_id,
            service_type=service_type,
            date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.PENDING,
            notes=notes,
            total_price=total_price,
            created_at=now,
            updated_at=now,
        )

    def _validate_transition(self, target_status: AppointmentStatus) -> None:
        """Validate that a state transition is allowed.

        Args:
            target_status: The desired new status.

        Raises:
            BusinessRuleError: If the transition is not allowed.
        """

        allowed = VALID_TRANSITIONS.get(self.status, [])

        if target_status not in allowed:
            raise BusinessRuleError(
                f"Cannot transition from {self.status.value} to {target_status.value}"
            )

    def _update_status(self, target_status: AppointmentStatus) -> None:
        """Update the status and timestamp after validation.

        Args:
            target_status: The new status to set.

        Raises:
            BusinessRuleError: If the transition is not allowed.
        """

        self._validate_transition(target_status)
        self.status = target_status
        self.updated_at = datetime.now()

    def accept(self) -> None:
        """Accept a pending appointment (PENDING -> CONFIRMED).

        Called by the artist when they accept the appointment request.

        Raises:
            BusinessRuleError: If the appointment is not in PENDING status.
        """

        self._update_status(AppointmentStatus.CONFIRMED)

    def reject(self) -> None:
        """Reject a pending appointment (PENDING -> CANCELLED).

        Called by the artist when they decline the appointment request.

        Raises:
            BusinessRuleError: If the appointment is not in PENDING status.
        """

        self._update_status(AppointmentStatus.CANCELLED)

    def start(self) -> None:
        """Start a confirmed appointment (CONFIRMED -> IN_PROGRESS).

        Called when the client arrives and the service begins.

        Raises:
            BusinessRuleError: If the appointment is not in CONFIRMED status.
        """

        self._update_status(AppointmentStatus.IN_PROGRESS)

    def complete(self) -> None:
        """Complete an in-progress appointment (IN_PROGRESS -> COMPLETED).

        Called when the service has been delivered successfully.

        Raises:
            BusinessRuleError: If the appointment is not in IN_PROGRESS status.
        """

        self._update_status(AppointmentStatus.COMPLETED)

    def cancel(self) -> None:
        """Cancel a pending or confirmed appointment.

        Valid from: PENDING or CONFIRMED -> CANCELLED

        Raises:
            BusinessRuleError: If the appointment cannot be cancelled
                (e.g., already completed or cancelled).
        """

        self._update_status(AppointmentStatus.CANCELLED)

    def mark_no_show(self) -> None:
        """Mark client as no-show (IN_PROGRESS -> NO_SHOW).

        Called when the client does not arrive for their appointment.

        Raises:
            BusinessRuleError: If the appointment is not in IN_PROGRESS status.
        """

        self._update_status(AppointmentStatus.NO_SHOW)

    def delete(self) -> None:
        """Delete the appointment.

        Only PENDING or CANCELLED appointments can be deleted.

        Raises:
            BusinessRuleError: If the appointment cannot be deleted.
        """

        if self.status not in (AppointmentStatus.PENDING, AppointmentStatus.CANCELLED):
            raise BusinessRuleError(
                f"Cannot delete appointment in {self.status.value} status"
            )

    def update_details(
        self,
        appointment_date: date | None = None,
        start_time: time | None = None,
        notes: str | None = None,
        total_price: float | None = None,
    ) -> None:
        """Update mutable appointment details.

        Only allowed when status is PENDING or CONFIRMED.
        Recalculates end_time if start_time changes.

        Args:
            appointment_date: New date (None = don't change).
            start_time: New start time (None = don't change).
            notes: New notes (None = don't change).
            total_price: New price (None = don't change).

        Raises:
            BusinessRuleError: If status is not PENDING or CONFIRMED.
            BusinessRuleError: If total_price is negative.
        """

        if self.status not in (AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED):
            raise BusinessRuleError(
                f"Cannot update details of appointment in {self.status.value} status"
            )

        if total_price is not None and total_price < 0:
            raise BusinessRuleError("Total price cannot be negative")

        if appointment_date is not None:
            self.date = appointment_date

        if start_time is not None:
            self.start_time = start_time
            # Recalculate end_time based on service duration
            duration_minutes = SERVICE_DURATIONS.get(self.service_type, 60)
            start_datetime = datetime.combine(self.date, self.start_time)
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)
            self.end_time = end_datetime.time()

        if notes is not None:
            self.notes = notes

        if total_price is not None:
            self.total_price = total_price

        self.updated_at = datetime.now()
