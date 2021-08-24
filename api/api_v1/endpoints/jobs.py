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
    "/job",
    response_model=schemas.Job,
    status_code=201
)
async def create_job(
        create_data: schemas.JobCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    try:
        return await crud.job.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.post(
    "/job/type",
    response_model=schemas.JobType,
    status_code=201
)
async def create_job_type(
        create_data: schemas.JobTypeCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user)
) -> Any:
    try:
        return await crud.job_type.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.get(
    "/jobs",
    response_model=List[schemas.Job]
)
async def get_jobs(
        user: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    # return await crud.job.get_multi(db)
    if await crud.user.is_manager_user(current_user):
        return await crud.job.get_list(db, user_id=user)
    return await crud.job.get_list(db, user_id=current_user.id)


@router.get(
    "/job/types",
    response_model=List[schemas.JobType]
)
async def get_job_types(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    return await crud.job_type.get_multi(db)


@router.delete(
    "/job",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def delete_job(
        id: int,
        admin: models.User = Depends(deps.get_current_admin_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    try:
        await crud.job.remove(db=db, id=id)
        return Response(status_code=204)
    except:
        raise NotFoundError(detail="Job not found")


@router.delete(
    "/job/type",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def delete_job_types(
        id: int,
        admin: models.User = Depends(deps.get_current_admin_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    try:
        await crud.job_type.remove(db=db, id=id)
        return Response(status_code=204)
    except:
        raise NotFoundError(detail="Job type not found")


@router.patch(
    "/job",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.Job
)
async def update_job(
        id: int,
        data: schemas.JobUpdate,
        user: models.User = Depends(deps.get_current_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    job = await crud.job.get(db=db, id=id)
    if job is None:
        raise NotFoundError("Job not found")
    try:
        return await crud.zone.update(db=db, db_obj=job, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.patch(
    "/job/type",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Job not found"},
    },
    response_model=schemas.JobType
)
async def update_job_type(
        id: int,
        data: schemas.ZoneTypeCreate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    job_type = await crud.job_type.get(db=db, id=id)
    if job_type is None:
        raise NotFoundError("Job not found")
    try:
        return await crud.job_type.update(db=db, db_obj=job_type, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)
