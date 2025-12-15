from fastapi import status
from fastapi.testclient import TestClient


class TestUsersEndpoint:
    def test_get_current_user(self, client: TestClient, auth_headers):
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert "email" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "disabled" in user_data
        assert "image_url" in user_data
        assert "password_hash" not in user_data

    def test_change_password(self, client: TestClient, auth_headers):
        # Change password
        response = client.put(
            "/api/v1/users/change-password",
            headers=auth_headers,
            json={
                "current_password": "Testpassword124",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        # Try logging in with new password
        login_response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "test@test.com",
                "password": "newpassword123",
                "grant_type": "password",
            },
        )
        assert login_response.status_code == status.HTTP_200_OK

    def test_password_change_validation(self, client: TestClient, auth_headers):
        # Test wrong current password
        response = client.put(
            "/api/v1/users/change-password",
            headers=auth_headers,
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test password mismatch
        response = client.put(
            "/api/v1/users/change-password",
            headers=auth_headers,
            json={
                "current_password": "Testpassword124",
                "new_password": "newpassword123",
                "new_password_confirm": "differentpassword123",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_endpoints_authorization(self, client: TestClient):
        # Try accessing user endpoints without auth
        response = client.get("/api/v1/users/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.put(
            "/api/v1/users/change-password",
            json={
                "current_password": "testpassword123",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
