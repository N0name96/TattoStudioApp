"""Integration tests for protected appointment endpoints."""

from fastapi.testclient import TestClient

from main import app


def create_user_and_login(client: TestClient, email: str, role: str):
    register_payload = {
        "email": email,
        "password": "StrongPass123",
        "full_name": "Protected User",
        "role": role,
        "phone": "555-0003",
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": register_payload["password"]},
    )
    assert login_response.status_code == 200

    return login_response.json()["data"]["access_token"]


def test_create_appointment_requires_auth():
    client = TestClient(app)

    response = client.post(
        "/api/v1/appointments/",
        json={
            "artist_id": "00000000-0000-0000-0000-000000000000",
            "service_type": "tattoo",
            "date": "2099-01-01",
            "start_time": "10:00:00",
            "notes": "Protected request",
        },
    )

    assert response.status_code == 401


def test_accept_appointment_requires_artist_or_admin():
    client = TestClient(app)
    client_token = create_user_and_login(client, "client-protected@example.com", "client")
    artist_token = create_user_and_login(client, "artist-protected@example.com", "artist")

    # Create the appointment as the client
    auth_headers = {"Authorization": f"Bearer {client_token}"}
    create_response = client.post(
        "/api/v1/appointments/",
        json={
            "artist_id": "00000000-0000-0000-0000-000000000000",
            "service_type": "tattoo",
            "date": "2099-01-01",
            "start_time": "10:00:00",
            "notes": "Protected accept",
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    appointment_id = create_response.json()["data"]["id"]

    # Client should not be allowed to accept
    client_response = client.put(
        f"/api/v1/appointments/{appointment_id}/accept",
        headers=auth_headers,
    )
    assert client_response.status_code == 403

    # Artist should be allowed to accept
    artist_headers = {"Authorization": f"Bearer {artist_token}"}
    artist_response = client.put(
        f"/api/v1/appointments/{appointment_id}/accept",
        headers=artist_headers,
    )
    assert artist_response.status_code == 200
