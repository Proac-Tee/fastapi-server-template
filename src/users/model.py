from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    image_url: str
    disabled: bool


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
