from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginDTO(BaseModel):
    username: str
    password: str


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    created_at: datetime


class LoginSuccessDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseDTO