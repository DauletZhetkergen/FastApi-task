from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    username: str
    password: str
    admin: bool = False


class UserBase(BaseModel):
    id: int
    username: str


class AuthData(BaseModel):
    username: str
    password: str


class TokenBase(BaseModel):
    token: UUID = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @field_validator("token")
    def hexlify_token(cls, value):
        if isinstance(value, UUID):
            return value.hex
        return value

class User(UserBase):
    token: TokenBase = {}
