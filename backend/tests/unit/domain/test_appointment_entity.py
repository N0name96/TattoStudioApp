"""Tests for the Appointment domain entity.

This module tests the pure business logic of the Appointment entity,
including creation, state transitions, and validation rules.

No mocks are needed since the entity has no external dependencies.
"""


from datetime import date, time, timedelta
from uuid import uuid4

import pytest

from core.errors import BusinessRuleError
from domain.entities.appointment_entity import Appointment
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


class TestAppointmentCreation:
    """Tests for Appointment.create() factory method."""

    def test_create_appointment_with_valid_data(self):
        """Test that a valid appointment can be created."""

        client_id = uuid4()
        artist_id = uuid4()
        appointment_date = date.today() + timedelta(days=7)

        appointment = Appointment.create(
            client_id=client_id,
            artist_id=artist_id,
            service_type=ServiceType.TATTOO,
            appointment_date=appointment_date,
            start_time=time(10, 0),
            notes="First session",
        )

        assert appointment.client_id == client_id
        assert appointment.artist_id == artist_id
        assert appointment.service_type == ServiceType.TATTOO
        assert appointment.date == appointment_date
        assert appointment.start_time == time(10, 0)
        assert appointment.status == AppointmentStatus.PENDING
        assert appointment.notes == "First session"
        assert appointment.total_price == 0.0

    def test_create_appointment_calculates_end_time_for_tattoo(self):
        """Test that end_time is calculated correctly for tattoo (120 min)."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(14, 0),
        )

        assert appointment.end_time == time(16, 0)

    def test_create_appointment_calculates_end_time_for_piercing(self):
        """Test that end_time is calculated correctly for piercing (30 min)."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.PIERCING,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        assert appointment.end_time == time(10, 30)

    def test_create_appointment_with_default_price(self):
        """Test that default price is 0.0."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        assert appointment.total_price == 0.0

    def test_create_appointment_has_unique_id(self):
        """Test that each appointment gets a unique ID."""

        appointment1 = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment2 = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        assert appointment1.id != appointment2.id


class TestAppointmentTransitions:
    """Tests for appointment state transitions."""

    def test_accept_pending_appointment(self):
        """Test accepting a pending appointment changes status to CONFIRMED."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()

        assert appointment.status == AppointmentStatus.CONFIRMED

    def test_reject_pending_appointment(self):
        """Test rejecting a pending appointment changes status to CANCELLED."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.reject()

        assert appointment.status == AppointmentStatus.CANCELLED

    def test_start_confirmed_appointment(self):
        """Test starting a confirmed appointment changes status to IN_PROGRESS."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()

        assert appointment.status == AppointmentStatus.IN_PROGRESS

    def test_complete_in_progress_appointment(self):
        """Test completing an in-progress appointment changes status to COMPLETED."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()
        appointment.complete()

        assert appointment.status == AppointmentStatus.COMPLETED

    def test_cancel_pending_appointment(self):
        """Test cancelling a pending appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.cancel()

        assert appointment.status == AppointmentStatus.CANCELLED

    def test_cancel_confirmed_appointment(self):
        """Test cancelling a confirmed appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.cancel()

        assert appointment.status == AppointmentStatus.CANCELLED

    def test_mark_no_show_in_progress_appointment(self):
        """Test marking an in-progress appointment as no-show."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()
        appointment.mark_no_show()

        assert appointment.status == AppointmentStatus.NO_SHOW


class TestInvalidTransitions:
    """Tests for invalid state transitions that should raise BusinessRuleError."""

    def test_cannot_accept_non_pending_appointment(self):
        """Test that accepting a non-pending appointment raises error."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()

        with pytest.raises(BusinessRuleError):
            appointment.accept()

    def test_cannot_start_non_confirmed_appointment(self):
        """Test that starting a non-confirmed appointment raises error."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        with pytest.raises(BusinessRuleError):
            appointment.start()

    def test_cannot_complete_non_in_progress_appointment(self):
        """Test that completing a non-in-progress appointment raises error."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        with pytest.raises(BusinessRuleError):
            appointment.complete()

    def test_cannot_cancel_completed_appointment(self):
        """Test that cancelling a completed appointment raises error."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()
        appointment.complete()

        with pytest.raises(BusinessRuleError):
            appointment.cancel()

    def test_cannot_cancel_already_cancelled_appointment(self):
        """Test that cancelling an already cancelled appointment raises error."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.cancel()

        with pytest.raises(BusinessRuleError):
            appointment.cancel()


class TestAppointmentUpdateDetails:
    """Tests for Appointment.update_details() method."""

    def test_update_details_on_pending_appointment(self):
        """Test that details can be updated on a PENDING appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            notes="Original notes",
        )

        new_date = date.today() + timedelta(days=14)
        appointment.update_details(
            appointment_date=new_date,
            start_time=time(14, 0),
            notes="Updated notes",
            total_price=150.0,
        )

        assert appointment.date == new_date
        assert appointment.start_time == time(14, 0)
        assert appointment.notes == "Updated notes"
        assert appointment.total_price == 150.0

    def test_update_details_on_confirmed_appointment(self):
        """Test that details can be updated on a CONFIRMED appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()

        appointment.update_details(total_price=200.0)

        assert appointment.total_price == 200.0

    def test_update_details_recalculates_end_time(self):
        """Test that end_time is recalculated when start_time changes."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        assert appointment.end_time == time(12, 0)

        appointment.update_details(start_time=time(14, 0))

        assert appointment.start_time == time(14, 0)
        assert appointment.end_time == time(16, 0)

    def test_update_details_partial_update(self):
        """Test that only provided fields are updated."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            notes="Original notes",
        )

        original_date = appointment.date
        original_start = appointment.start_time

        appointment.update_details(notes="Updated notes")

        assert appointment.date == original_date
        assert appointment.start_time == original_start
        assert appointment.notes == "Updated notes"

    def test_update_details_cannot_update_completed_appointment(self):
        """Test that details cannot be updated on a COMPLETED appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()
        appointment.complete()

        with pytest.raises(BusinessRuleError):
            appointment.update_details(notes="Should fail")

    def test_update_details_cannot_update_cancelled_appointment(self):
        """Test that details cannot be updated on a CANCELLED appointment."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.cancel()

        with pytest.raises(BusinessRuleError):
            appointment.update_details(notes="Should fail")

    def test_update_details_cannot_set_negative_price(self):
        """Test that total_price cannot be set to negative."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        with pytest.raises(BusinessRuleError):
            appointment.update_details(total_price=-10.0)


class TestAppointmentDelete:
    """Tests for Appointment.delete() method."""

    def test_delete_pending_appointment(self):
        """Test that a PENDING appointment can be deleted."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.delete()

    def test_delete_cancelled_appointment(self):
        """Test that a CANCELLED appointment can be deleted."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.cancel()
        appointment.delete()

    def test_cannot_delete_confirmed_appointment(self):
        """Test that a CONFIRMED appointment cannot be deleted."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()

        with pytest.raises(BusinessRuleError):
            appointment.delete()

    def test_cannot_delete_in_progress_appointment(self):
        """Test that an IN_PROGRESS appointment cannot be deleted."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()

        with pytest.raises(BusinessRuleError):
            appointment.delete()

    def test_cannot_delete_completed_appointment(self):
        """Test that a COMPLETED appointment cannot be deleted."""

        appointment = Appointment.create(
            client_id=uuid4(),
            artist_id=uuid4(),
            service_type=ServiceType.TATTOO,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
        )

        appointment.accept()
        appointment.start()
        appointment.complete()

        with pytest.raises(BusinessRuleError):
            appointment.delete()
