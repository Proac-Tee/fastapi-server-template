from uuid import UUID

from fastapi import APIRouter, status

from src.auth.service import CurrentUser
from src.database.core import DbSession
from src.users import model, service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=model.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    user_id = UUID(current_user.user_id)
    return service.get_user_by_id(db, user_id)


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_change: model.PasswordChange, db: DbSession, current_user: CurrentUser
):
    user_id = UUID(current_user.user_id)
    service.change_password(db, user_id, password_change)
