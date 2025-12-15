import pytest
from sqlalchemy.orm import Session

from src.auth import service as auth_service
from src.entities.user import User
from src.exceptions import (
    InvalidPasswordError,
    PasswordMismatchError,
    UserNotFoundError,
)
from src.users import service as user_service
from src.users.model import PasswordChange


class TestUserServive:
    def test_get_user_by_id(self, db_session: Session, test_user: User):
        db_session.add(test_user)
        db_session.commit()

        user = user_service.get_user_by_id(db_session, test_user.id)
        assert user.id == test_user.id
        assert user.email == test_user.email

        with pytest.raises(UserNotFoundError):
            user_service.get_user_by_id(db_session, 2)

    def test_change_password(self, db_session: Session, test_user: User):
        db_session.add(test_user)
        db_session.commit()

        password_change = PasswordChange(
            current_password="Testpassword124",
            new_password="newpassword123",
            new_password_confirm="newpassword123",
        )

        user_service.change_password(db_session, test_user.id, password_change)

        updated_user = db_session.query(User).filter_by(id=test_user.id).first()

        assert updated_user is not None, "User not found in DB after change_password"

        assert auth_service.verify_password(
            "newpassword123", updated_user.password_hash
        )

    def test_change_password_invalid_current(
        self, db_session: Session, test_user: User
    ):
        db_session.add(test_user)
        db_session.commit()

        with pytest.raises(InvalidPasswordError):
            password_change = PasswordChange(
                current_password="WrongPassword124",
                new_password="newpassword123",
                new_password_confirm="newpassword123",
            )

            user_service.change_password(db_session, test_user.id, password_change)

    def test_change_password_mismatch(self, db_session: Session, test_user: User):
        db_session.add(test_user)
        db_session.commit()

        with pytest.raises(PasswordMismatchError):
            password_change = PasswordChange(
                current_password="Testpassword124",
                new_password="newpassword123",
                new_password_confirm="diffrentpassword124",
            )

            user_service.change_password(db_session, test_user.id, password_change)
