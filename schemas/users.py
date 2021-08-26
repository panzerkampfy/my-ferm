from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas import APIModel


class UserCreate(APIModel):
    first_name: str
    middle_name: str
    last_name: str
    role_id: int


class User(UserCreate):
    id: int
    login: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class UserUpdate(APIModel):
    login: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    role_id: Optional[int]


class ResetPassword(APIModel):
    password: str


class TokenLogin(APIModel):
    login: str
    password: str


class Token(APIModel):
    user: User
    access_token: str
    token_type: str


class TokenPayload(APIModel):
    sub: int


class OAuth2ComplaintToken(BaseModel):
    access_token: str
    token_type: str

