from fastapi import status
from fastapi.testclient import TestClient

from src.auth.model import RegisterUserRequest


class TestAuthEndpoints:
    def test_register_and_login_flow(self, client: TestClient):
        register_data = RegisterUserRequest(
            email="test.user@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User",
            image_url="imagel.url",
        )

        response = client.post("/api/v1/auth/", json=register_data.model_dump())
        assert response.status_code == status.HTTP_201_CREATED

        # Test successful login
        login_response = client.post(
            "/api/v1/auth/token",
            data={
                "username": register_data.email,
                "password": register_data.password,
                "grant_type": "password",
            },
        )

        assert login_response.status_code == status.HTTP_200_OK
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

    def test_login_failures(self, client: TestClient):
        # Test login with non-existent user
        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "nonexistent@example.com",
                "password": "wrongpassword",
                "grant_type": "password",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test login with wrong password
        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "test.user@example.com",
                "password": "wrongpassword",
                "grant_type": "password",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rate_limiting(self, client: TestClient):
        # Test rate limiting on registration
        for _ in range(5):  # Attempt 4 registrations (limit is 5/hour)
            response = client.post(
                "/api/v1/auth/",
                json={
                    "email": f"test{_}@example.com",
                    "password": "testpassword123",
                    "first_name": "Test",
                    "last_name": "User",
                },
            )
            assert response.status_code == status.HTTP_201_CREATED

        # Attemp the 5th registration which exceeds the limit
        response = client.post(
            "/api/v1/auth/",
            json={
                "email": "test5@example.com",
                "password": "testpassword123",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
