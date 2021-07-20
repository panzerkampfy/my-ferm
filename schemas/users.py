import re
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from schemas import APIModel, Category, City, Gender, Role, Subject
from pydantic import BaseModel, EmailStr, validator


class UserBase(APIModel):
    email: EmailStr
    first_name: str
    middle_name: str
    last_name: str
    birth_date: date
    phone: Optional[str]


class UserCreate(UserBase):
    first_name: str
    middle_name: str
    last_name: str
    role: Optional[Role]


class User(UserBase):
    """
    A model for User.
    """

    id: int
    first_name: str
    middle_name: str
    last_name: str
    login: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    role: Optional[Role]


class TokenLogin(APIModel):
    """
    A model for login requests.
    """

    login: str
    password: str


class Token(APIModel):
    """
    A model for providing token and user info after authentication.
    """

    user: User
    access_token: str
    token_type: str


class OAuth2ComplaintToken(BaseModel):
    """
    A model for token response.
    Note: access_token and token_type is snake case because of RFC6749 section 4.1.4
    """

    access_token: str
    token_type: str


class TokenPayload(APIModel):
    sub: UUID
