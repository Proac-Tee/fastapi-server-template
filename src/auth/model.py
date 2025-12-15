from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    image_url: str = ""
    disabled: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None

    def get_user_id(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None
