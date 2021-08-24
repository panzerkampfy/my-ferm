from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response

import crud
import models
from api import deps
from sqlalchemy.orm import Session

import schemas
from api.api_v1.exceptions import NotFoundError

router = APIRouter()


@router.post(
    "/role",
    response_model=schemas.Role,
    status_code=201
)
async def role_create(
    role_data: schemas.RoleCreate,
    db: Session = Depends(deps.get_db),
    manager: models.User = Depends(deps.get_current_manager_user)
) -> schemas.Role:
    return await crud.role.create(db, obj_in=role_data)


@router.get(
    "/roles",
    response_model=List[schemas.Role]
)
async def get_roles(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    return await crud.role.get_multi(db)


@router.delete(
    "/role",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def delete_role(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    try:
        await crud.role.remove(db=db, id=id)
        return Response(status_code=204)
    except:
        raise NotFoundError(detail="Role not found")


@router.patch(
    "/role",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.Role
)
async def update_role(
        id: int,
        data: schemas.RoleCreate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    role = await crud.role.get(db=db, id=id)
    if role is None:
        raise NotFoundError("Role not found")
    return await crud.zone_type.update(db=db, db_obj=role, obj_in=data)
