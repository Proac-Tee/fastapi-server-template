from fastapi import HTTPException, status


class UserError(HTTPException):
    """
    Base exception for all user-related errors.
    Extends FastAPI's HTTPException for consistent API responses.
    """

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundError(UserError):
    def __init__(self, user_id: str | None = None):
        message = (
            "User not found"
            if user_id is None
            else f"User with id '{user_id}' not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class InactiveUserError(UserError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )


class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match",
        )


class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )


class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
