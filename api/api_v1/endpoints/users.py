from typing import Any, List
from fastapi import APIRouter, Depends

import crud
import models
import schemas
from api import deps
from sqlalchemy.orm import Session

from api.api_v1.exceptions import NotFoundError

router = APIRouter()


@router.get(
    "/users",
    response_model=List[schemas.User],
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def read_users(
    role_id: int,
    db: Session = Depends(deps.get_db),
    manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    workers = await crud.user.get_by_role(db, role=role_id)
    return workers


@router.get(
    "/user",
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def read_users(
    user_id: int,
    db: Session = Depends(deps.get_db),
    manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    user = await crud.user.get(db, id=user_id)
    jobs = await crud.job.get_list_by_user(db, user=user_id)
    return {
        "user": user,
        "jobs": jobs
        }


@router.patch(
    "/user",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.User
)
async def update_user(
    id: int,
    data: schemas.UserUpdate,
    manager: models.User = Depends(deps.get_current_manager_user),
    db: Session = Depends(deps.get_db)
) -> schemas.User:
    user = await crud.user.get(db=db, id=id)
    try:
        return await crud.user.update(db=db, db_obj=user, obj_in=data)
    except:
        raise NotFoundError(detail="Role not found")


@router.patch(
    "/user/password",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.User
)
async def reset_password(
    data: schemas.ResetPassword,
    user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> schemas.User:
    return await crud.user.update(db=db, db_obj=user, obj_in=data)
