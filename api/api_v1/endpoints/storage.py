import re
from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response

import crud
import models
import schemas
from api import deps
from sqlalchemy.orm import Session

from api.api_v1.exceptions import NotFoundError

router = APIRouter()


@router.post(
    "/storage",
    response_model=schemas.Storage,
    status_code=201
)
async def create_storage_product(
        create_data: schemas.StorageCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    try:
        return await crud.storage.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.get(
    "/storage",
    response_model=List[schemas.Storage]
)
async def get_products_from_storage(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    return await crud.storage.get_multi(db)


@router.delete(
    "/storage",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Job not found"},
    },
)
async def delete_storage_product(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    try:
        await crud.storage.remove(db=db, id=id)
        return Response(status_code=204)
    except:
        raise NotFoundError(detail="Zone not found")


@router.patch(
    "/storage",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Job not found"},
    },
    response_model=schemas.Storage
)
async def update_storage_product(
        id: int,
        data: schemas.StorageUpdate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    storage = await crud.storage.get(db=db, id=id)
    if storage is None:
        raise NotFoundError("Storage not found")
    try:
        return await crud.storage.update(db=db, db_obj=storage, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)
