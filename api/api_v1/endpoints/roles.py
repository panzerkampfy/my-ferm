from fastapi import APIRouter, Depends, HTTPException

import crud
from api import deps
from sqlalchemy.orm import Session

import schemas

router = APIRouter()


@router.post(
    "/role",
    response_model=schemas.Role,
    status_code=201
)
async def add_role(
    role_data: schemas.RoleCreate, db: Session = Depends(deps.get_db)
) -> schemas.Role:
    role = await crud.CRUDRole.create(db, obj_in=role_data)
    return role
