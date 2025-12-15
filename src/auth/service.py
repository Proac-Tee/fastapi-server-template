import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID, uuid4

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy.orm.session import Session

from src.database.core import get_db
from src.entities.user import User
from src.exceptions import AuthenticationError
from src.settings import settings

from . import model

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


password_hash = PasswordHash.recommended()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logging.warning(f"Authentication failed: user not found ({email})")
        return None

    if not verify_password(password, user.password_hash):
        logging.warning(f"Authentication failed: incorrect password ({email})")
        return None

    return user


def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        "sub": email,
        "id": str(user_id),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> model.TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)

        user_id = payload.get("id")
        if not user_id:
            logging.warning(f"Invalid token - missing user id")
            raise AuthenticationError("Invalid token: missing user id")

        return model.TokenData(user_id=user_id)

    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(
    db: Session, register_user_request: model.RegisterUserRequest
) -> None:
    """
    Registers a new user in the database.
    """
    try:
        new_user = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password_hash=get_password_hash(register_user_request.password),
            image_url=register_user_request.image_url,
            disabled=False,
        )
        db.add(new_user)
        db.commit()
    except Exception as e:
        logging.error(
            f"Failed to register user: {register_user_request.email}, Error: {str(e)}"
        )
        raise


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> model.TokenData:
    return verify_token(token)


CurrentUser = Annotated[model.TokenData, Depends(get_current_user)]


def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> model.Token:
    """
    Authenticate user and return JWT access token.
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise AuthenticationError()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        user.email, user.id, expires_delta=access_token_expires
    )

    return model.Token(
        access_token=access_token,
        token_type="bearer",
    )
