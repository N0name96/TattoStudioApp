"""Integration tests for authentication endpoints."""

from fastapi.testclient import TestClient

from main import app


def test_register_and_login_success():
    client = TestClient(app)

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "password": "StrongPass123",
            "full_name": "User Example",
            "role": "client",
            "phone": "555-0001",
        },
    )

    assert register_response.status_code == 201
    assert register_response.json()["success"] is True
    assert register_response.json()["data"]["email"] == "user@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "StrongPass123"},
    )

    assert login_response.status_code == 200
    login_data = login_response.json()["data"]
    assert login_data["access_token"]
    assert login_data["refresh_token"]
    assert login_data["token_type"] == "bearer"

    access_token = login_data["access_token"]
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["data"]["email"] == "user@example.com"


def test_refresh_token_success():
    client = TestClient(app)

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh@example.com",
            "password": "StrongPass123",
            "full_name": "Refresh User",
            "role": "client",
            "phone": "555-0002",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "refresh@example.com", "password": "StrongPass123"},
    )
    assert login_response.status_code == 200

    refresh_token = login_response.json()["data"]["refresh_token"]
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert refresh_response.status_code == 200
    assert refresh_response.json()["data"]["access_token"]
    assert refresh_response.json()["data"]["refresh_token"]
