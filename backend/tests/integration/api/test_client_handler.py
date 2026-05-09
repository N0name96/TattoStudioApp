"""Integration tests for the client API endpoints.

This module tests the full request cycle from API handler through use case
to in-memory repository, verifying all 5 endpoints end-to-end.
"""


import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(autouse=True)
def reset_container():
    """Reset the DI container repository before each test."""

    from core.container import container

    container._client_repository = None
    container._user_repository = None
    container._security_service = None
    yield
    container._client_repository = None
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


class TestCreateClientEndpoint:
    """Tests for POST /clients/."""

    def test_create_client_success(self, client):
        response = client.post(
            "/api/v1/clients/",
            json={
                "full_name": "John Doe",
                "email": "john.unique@example.com",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["full_name"] == "John Doe"
        assert data["data"]["email"] == "john.unique@example.com"

    def test_create_client_duplicate_email(self, client):
        client.post(
            "/api/v1/clients/",
            json={
                "full_name": "First",
                "email": "dup@example.com",
            },
        )
        response = client.post(
            "/api/v1/clients/",
            json={
                "full_name": "Second",
                "email": "dup@example.com",
            },
        )

        assert response.status_code == 409

    def test_create_client_validation_error(self, client):
        response = client.post(
            "/api/v1/clients/",
            json={"full_name": ""},
        )
        assert response.status_code == 422


class TestListClientsEndpoint:
    """Tests for GET /clients/."""

    def test_list_clients_empty(self, client):
        response = client.get("/api/v1/clients/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == []

    def test_list_clients_with_data(self, client):
        client.post(
            "/api/v1/clients/",
            json={
                "full_name": "Test Client",
                "email": "list@example.com",
            },
        )
        response = client.get("/api/v1/clients/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["full_name"] == "Test Client"


class TestGetClientEndpoint:
    """Tests for GET /clients/{id}."""

    def test_get_client_success(self, client):
        create_resp = client.post(
            "/api/v1/clients/",
            json={
                "full_name": "Get Me",
                "email": "getme@example.com",
            },
        )
        client_id = create_resp.json()["data"]["id"]

        response = client.get(f"/api/v1/clients/{client_id}")
        assert response.status_code == 200
        assert response.json()["data"]["full_name"] == "Get Me"

    def test_get_client_not_found(self, client):
        response = client.get("/api/v1/clients/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestUpdateClientEndpoint:
    """Tests for PUT /clients/{id}."""

    def test_update_client_success(self, client):
        create_resp = client.post(
            "/api/v1/clients/",
            json={
                "full_name": "Old Name",
                "email": "update@example.com",
            },
        )
        client_id = create_resp.json()["data"]["id"]

        response = client.put(
            f"/api/v1/clients/{client_id}",
            json={"full_name": "New Name"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["full_name"] == "New Name"

    def test_update_client_not_found(self, client):
        response = client.put(
            "/api/v1/clients/00000000-0000-0000-0000-000000000000",
            json={"full_name": "Nope"},
        )
        assert response.status_code == 404


class TestDeleteClientEndpoint:
    """Tests for DELETE /clients/{id}."""

    def test_delete_client_success(self, client):
        create_resp = client.post(
            "/api/v1/clients/",
            json={
                "full_name": "To Delete",
                "email": "delete@example.com",
            },
        )
        client_id = create_resp.json()["data"]["id"]

        response = client.delete(f"/api/v1/clients/{client_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Client deleted successfully"

    def test_delete_client_not_found(self, client):
        response = client.delete("/api/v1/clients/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
