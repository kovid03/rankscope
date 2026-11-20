"""
Pydantic v2 schemas for authentication endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}
