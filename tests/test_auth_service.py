from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import service as auth_service
from src.auth.model import RegisterUserRequest, TokenData
from src.entities.user import User
from src.exceptions import AuthenticationError


class TestAuthService:
    def test_verify_password(self):
        plain_password = "Testpassword123"
        hashed_password = auth_service.get_password_hash(plain_password)
        assert auth_service.verify_password(plain_password, hashed_password)
        assert not auth_service.verify_password("WrongPassword12", hashed_password)

    def test_authenticate_user(self, db_session: Session, test_user: User):
        db_session.add(test_user)
        db_session.commit()

        correct_user = auth_service.authenticate_user(
            "test@test.com", "Testpassword124", db_session
        )
        wrong_user = auth_service.authenticate_user(
            "fake@test.com", "Testpassword124", db_session
        )

        wrong_password = auth_service.authenticate_user(
            "test@test.com", "WrongPassword124", db_session
        )

        assert correct_user is not None
        assert correct_user.email == test_user.email
        assert wrong_user is None
        assert wrong_password is None

    def test_login_for_access_token(self, db_session: Session, test_user: User):
        db_session.add(test_user)
        db_session.commit()

        form_data = OAuth2PasswordRequestForm(
            username="test@test.com",
            password="Testpassword124",
            scope="",
            client_id=None,
            client_secret=None,
        )
        token = auth_service.login_for_access_token(form_data, db_session)
        assert token.token_type == "bearer"
        assert token.access_token is not None

    @pytest.mark.asyncio
    async def test_register_user(self, db_session: Session):
        request = RegisterUserRequest(
            email="new@example.com",
            password="password123",
            first_name="New",
            last_name="User",
            image_url="image.url",
        )
        auth_service.register_user(db_session, request)

        user = db_session.query(User).filter_by(email="new@example.com").first()

        assert user is not None
        assert user.email == "new@example.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.image_url == "image.url"

    def test_create_and_verify_token(self, db_session):
        user_id = uuid4()
        email = "text@example.com"

        access_token_expires = timedelta(minutes=30)

        token = auth_service.create_access_token(
            email, user_id, expires_delta=access_token_expires
        )

        token_data: TokenData = auth_service.verify_token(token)

        assert token_data.get_user_id() == user_id

        assert (
            auth_service.authenticate_user(
                "test@example.com", "wrongpassword", db_session
            )
            is None
        )

        with pytest.raises(AuthenticationError):
            form_data = OAuth2PasswordRequestForm(
                username="test@example.com", password="wrongpassword", scope=""
            )
            auth_service.login_for_access_token(form_data, db_session)
