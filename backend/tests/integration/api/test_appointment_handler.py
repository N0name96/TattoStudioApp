"""Integration tests for appointment API endpoints.

This module tests the full request cycle from API handler through use case
to in-memory repository, verifying all 11 endpoints end-to-end.
"""

from datetime import date, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from infrastructure.persistence.in_memory.appointment_repository import (
    InMemoryAppointmentRepository,
)
from main import app


@pytest.fixture(autouse=True)
def reset_container():
    """Reset the DI container repository before each test."""

    from core.container import container

    container._appointment_repository = None
    container._user_repository = None
    container._security_service = None
    yield
    container._appointment_repository = None
    container._user_repository = None
    container._security_service = None


@pytest.fixture
def client():
    """Create a FastAPI test client with an authenticated admin user."""

    client = TestClient(app)
    admin_payload = {
        "email": "admin@example.com",
        "password": "SuperSecret123",
        "full_name": "Admin User",
        "role": "admin",
        "phone": "1234567890",
    }

    register_response = client.post("/api/v1/auth/register", json=admin_payload)
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": admin_payload["email"], "password": admin_payload["password"]},
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["data"]["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest.fixture
def repo():
    """Create a fresh in-memory repository."""

    return InMemoryAppointmentRepository()


@pytest.fixture
def sample_client_id():
    """A sample client UUID for testing."""

    return uuid4()


@pytest.fixture
def sample_artist_id():
    """A sample artist UUID for testing."""

    return uuid4()


def _create_appointment_via_api(
    client: TestClient,
    artist_id: str,
    service_type: str = "tattoo",
    date_str: str = None,
    start_time: str = "10:00:00",
) -> dict:
    """Helper to create an appointment via the API."""

    if date_str is None:
        date_str = (date.today() + timedelta(days=7)).isoformat()

    response = client.post(
        "/api/v1/appointments/",
        json={
            "artist_id": artist_id,
            "service_type": service_type,
            "date": date_str,
            "start_time": start_time,
            "notes": "Test appointment",
        },
    )

    return response.json()


class TestCreateAppointmentEndpoint:
    """Tests for POST /api/v1/appointments/ endpoint."""

    def test_create_appointment_success(self, client):
        """Test successful appointment creation."""

        artist_id = str(uuid4())
        response = _create_appointment_via_api(client, artist_id)

        assert response["success"] is True
        assert response["data"]["artist_id"] == artist_id
        assert response["data"]["status"] == "pending"
        assert response["message"] == "Appointment created successfully"

    def test_create_appointment_returns_201(self, client):
        """Test that creation returns 201 status code."""

        artist_id = str(uuid4())
        response = client.post(
            "/api/v1/appointments/",
            json={
                "artist_id": artist_id,
                "service_type": "tattoo",
                "date": (date.today() + timedelta(days=7)).isoformat(),
                "start_time": "10:00:00",
            },
        )

        assert response.status_code == 201


class TestListAppointmentsEndpoint:
    """Tests for GET /api/v1/appointments/ endpoint."""

    def test_list_appointments_empty(self, client):
        """Test listing appointments when none exist."""

        response = client.get("/api/v1/appointments/")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == []

    def test_list_appointments_with_data(self, client):
        """Test listing appointments after creating some."""

        artist_id = str(uuid4())
        _create_appointment_via_api(client, artist_id)
        _create_appointment_via_api(client, artist_id, start_time="14:00:00")

        response = client.get("/api/v1/appointments/")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2


class TestGetAppointmentEndpoint:
    """Tests for GET /api/v1/appointments/{appointment_id} endpoint."""

    def test_get_appointment_success(self, client):
        """Test successful appointment retrieval."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.get(f"/api/v1/appointments/{appointment_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == appointment_id

    def test_get_appointment_not_found(self, client):
        """Test retrieval of non-existent appointment returns 404."""

        fake_id = str(uuid4())
        response = client.get(f"/api/v1/appointments/{fake_id}")

        assert response.status_code == 404


class TestAcceptAppointmentEndpoint:
    """Tests for PUT /api/v1/appointments/{id}/accept endpoint."""

    def test_accept_appointment_success(self, client):
        """Test successful appointment acceptance."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.put(f"/api/v1/appointments/{appointment_id}/accept")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "confirmed"
        assert data["message"] == "Appointment accepted"

    def test_accept_nonexistent_appointment(self, client):
        """Test accepting non-existent appointment returns 404."""

        fake_id = str(uuid4())
        response = client.put(f"/api/v1/appointments/{fake_id}/accept")

        assert response.status_code == 404


class TestRejectAppointmentEndpoint:
    """Tests for PUT /api/v1/appointments/{id}/reject endpoint."""

    def test_reject_appointment_success(self, client):
        """Test successful appointment rejection."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.put(f"/api/v1/appointments/{appointment_id}/reject")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "cancelled"
        assert data["message"] == "Appointment rejected"


class TestStartAppointmentEndpoint:
    """Tests for PUT /api/v1/appointments/{id}/start endpoint."""

    def test_start_appointment_success(self, client):
        """Test successful appointment start."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        # Accept first
        client.put(f"/api/v1/appointments/{appointment_id}/accept")

        # Then start
        response = client.put(f"/api/v1/appointments/{appointment_id}/start")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "in_progress"
        assert data["message"] == "Appointment started"

    def test_start_pending_appointment_fails(self, client):
        """Test that starting a pending appointment returns 422."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.put(f"/api/v1/appointments/{appointment_id}/start")

        assert response.status_code == 422


class TestCompleteAppointmentEndpoint:
    """Tests for PUT /api/v1/appointments/{id}/complete endpoint."""

    def test_complete_appointment_success(self, client):
        """Test successful appointment completion."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        # Accept -> Start -> Complete
        client.put(f"/api/v1/appointments/{appointment_id}/accept")
        client.put(f"/api/v1/appointments/{appointment_id}/start")

        response = client.put(f"/api/v1/appointments/{appointment_id}/complete")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "completed"
        assert data["message"] == "Appointment completed"


class TestCancelAppointmentEndpoint:
    """Tests for PUT /api/v1/appointments/{id}/cancel endpoint."""

    def test_cancel_appointment_success(self, client):
        """Test successful appointment cancellation."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.put(f"/api/v1/appointments/{appointment_id}/cancel")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "cancelled"
        assert data["message"] == "Appointment cancelled"


class TestUpdateAppointmentEndpoint:
    """Tests for PATCH /api/v1/appointments/{id} endpoint."""

    def test_update_appointment_success(self, client):
        """Test successful appointment details update."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.patch(
            f"/api/v1/appointments/{appointment_id}",
            json={
                "notes": "Updated notes",
                "total_price": 150.0,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["notes"] == "Updated notes"
        assert data["data"]["total_price"] == 150.0
        assert data["message"] == "Appointment updated successfully"

    def test_update_appointment_not_found(self, client):
        """Test updating non-existent appointment returns 404."""

        fake_id = str(uuid4())
        response = client.patch(
            f"/api/v1/appointments/{fake_id}",
            json={"notes": "Updated"},
        )

        assert response.status_code == 404

    def test_update_completed_appointment_fails(self, client):
        """Test that updating a completed appointment returns 422."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        # Complete the appointment
        client.put(f"/api/v1/appointments/{appointment_id}/accept")
        client.put(f"/api/v1/appointments/{appointment_id}/start")
        client.put(f"/api/v1/appointments/{appointment_id}/complete")

        # Try to update
        response = client.patch(
            f"/api/v1/appointments/{appointment_id}",
            json={"notes": "Should fail"},
        )

        assert response.status_code == 422


class TestDeleteAppointmentEndpoint:
    """Tests for DELETE /api/v1/appointments/{id} endpoint."""

    def test_delete_appointment_success(self, client):
        """Test successful appointment deletion."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.delete(f"/api/v1/appointments/{appointment_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Appointment deleted successfully"

        # Verify it's gone
        get_response = client.get(f"/api/v1/appointments/{appointment_id}")
        assert get_response.status_code == 404

    def test_delete_appointment_not_found(self, client):
        """Test deleting non-existent appointment returns 404."""

        fake_id = str(uuid4())
        response = client.delete(f"/api/v1/appointments/{fake_id}")

        assert response.status_code == 404

    def test_delete_completed_appointment_fails(self, client):
        """Test that deleting a completed appointment returns 422."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        # Complete the appointment
        client.put(f"/api/v1/appointments/{appointment_id}/accept")
        client.put(f"/api/v1/appointments/{appointment_id}/start")
        client.put(f"/api/v1/appointments/{appointment_id}/complete")

        # Try to delete
        response = client.delete(f"/api/v1/appointments/{appointment_id}")

        assert response.status_code == 422


class TestMarkNoShowEndpoint:
    """Tests for PUT /api/v1/appointments/{id}/no-show endpoint."""

    def test_mark_no_show_success(self, client):
        """Test successful no-show marking."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        # Accept -> Start -> No-show
        client.put(f"/api/v1/appointments/{appointment_id}/accept")
        client.put(f"/api/v1/appointments/{appointment_id}/start")

        response = client.put(f"/api/v1/appointments/{appointment_id}/no-show")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "no_show"
        assert data["message"] == "Appointment marked as no-show"

    def test_mark_no_show_pending_fails(self, client):
        """Test that marking a pending appointment as no-show returns 422."""

        artist_id = str(uuid4())
        create_response = _create_appointment_via_api(client, artist_id)
        appointment_id = create_response["data"]["id"]

        response = client.put(f"/api/v1/appointments/{appointment_id}/no-show")

        assert response.status_code == 422

    def test_mark_no_show_not_found(self, client):
        """Test marking non-existent appointment as no-show returns 404."""

        fake_id = str(uuid4())
        response = client.put(f"/api/v1/appointments/{fake_id}/no-show")

        assert response.status_code == 404
