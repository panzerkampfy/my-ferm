from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

import crud
import models
import schemas
from api import deps
from api.api_v1.exceptions import ValidationError
from core import security
from core.config import settings
from sqlalchemy.orm import Session
from utils import has_cyr

router = APIRouter()


def response_login(user):
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
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
    status_code=201
)
async def register(
        signup_data: schemas.UserCreate,
        db: Session = Depends(deps.get_db),
        admin: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    last_name = jsonable_encoder(signup_data, by_alias=False)['last_name']
    if not has_cyr(last_name):
        print(last_name)
        return ValidationError(detail="First, middle and last name must be Russian language")
    try:
        return await crud.user.create(db, obj_in=signup_data)
    except IntegrityError:
        ValidationError(detail="Login must be unique")


@router.post(
    "/token",
    response_model=schemas.Token,
)
async def token_login(
        login_data: schemas.TokenLogin,
        db: Session = Depends(deps.get_db)
) -> Any:
    user = await crud.user.authenticate(
        db, username=login_data.login, password=login_data.password
    )
    return response_login(user)


@router.post(
    "/login/oauth",
    response_model=schemas.OAuth2ComplaintToken,
    responses={
        400: {"model": schemas.GenericHTTPError, "description": "Invalid credentials"},
    },
)
async def oauth_login(
    db: Session = Depends(deps.get_db),
    login_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, username=login_data.username, password=login_data.password
    )
    return response_login(user)


