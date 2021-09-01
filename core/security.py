import random
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=(4 if settings.ENV_NAME == "test" else 11),
)
ALGORITHM = "HS256"


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_password() -> str:
    chars = '/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 8
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password


def verify_password(plain_password: str, true_password: str) -> bool:
    return plain_password == true_password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
