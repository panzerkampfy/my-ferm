from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import crud
import schemas
from api import deps
from core import security
from core.config import settings
from sqlalchemy.orm import Session

router = APIRouter()


def response_login(user):
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "user": user,
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }



@router.post(
    "/signup",
    response_model=schemas.Token,
)
async def register(
    signup_data: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> Any:
    """
    Registers user and returns JWT access token for future requests
    """
    user = await crud.user.create(db, obj_in=signup_data)
    return response_login(user)
