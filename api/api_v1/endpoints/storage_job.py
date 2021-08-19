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
    "/storage_job",
    response_model=schemas.StorageJob,
)
async def create_storage_job(
        create_data: schemas.StorageJobCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    try:
        return await crud.storage_job.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.get(
    "/storage_jobs",
    response_model=List[schemas.StorageJob]
)
async def get_storage_jobs(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    return await crud.storage_job.get_multi(db)


@router.delete(
    "/storage_job",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def delete_storage_job(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    try:
        await crud.storage_job.remove(db=db, id=id)
        return Response(status_code=204)
    except:
        raise NotFoundError(detail="Storage job not found")


@router.patch(
    "/storage_job",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.StorageJob
)
async def update_storage_job(
        id: int,
        data: schemas.StorageJobUpdate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    storage_job = await crud.storage_job.get(db=db, id=id)
    if storage_job is None:
        raise NotFoundError("Storage job not found")
    try:
        return await crud.storage_job.update(db=db, db_obj=storage_job, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)
