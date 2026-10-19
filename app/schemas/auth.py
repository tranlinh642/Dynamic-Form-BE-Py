from typing import List
import uuid
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(
        min_length=5,
        max_length=100,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
    )
    password: str = Field(min_length=6, max_length=100)


class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    isActive: bool

    class Config:
        from_attributes = True


class CurrentUserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    isActive: bool
    roles: List[str]
    permissions: List[str]

    class Config:
        from_attributes = True
