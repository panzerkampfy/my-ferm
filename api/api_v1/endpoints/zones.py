import re
from typing import Any, List, Optional
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
    "/zone",
    response_model=schemas.Zone,
)
async def create_zone(
        create_data: schemas.ZoneCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    try:
        return await crud.zone.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.post(
    "/zone/type",
    response_model=schemas.ZoneType,
)
async def create_zone_type(
        create_data: schemas.ZoneTypeCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    return await crud.zone_type.create(db, obj_in=create_data)


@router.get(
    "/zones",
    response_model=List[schemas.Zone]
)
async def get_zones(
        type: Optional[int] = None,
        user: Optional[int] = None,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    if await crud.user.is_manager_user(current_user):
        return await crud.zone.get_list(db, user_id=user, type_id=type)
    return await crud.zone.get_list(db, user_id=current_user.id)


@router.get(
    "/zone/types",
    response_model=List[schemas.ZoneType]
)
async def get_zone_types(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    return await crud.zone_type.get_multi(db)


@router.delete(
    "/zone",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Zone not found"},
    },
)
async def delete_zone(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    try:
        await crud.zone.remove(db=db, id=id)
    except:
        raise NotFoundError(detail="Zone not found")


@router.delete(
    "/zone/type",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def delete_zone_types(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    try:
        await crud.zone_type.remove(db=db, id=id)
        return Response(status_code=204)
    except:
        raise NotFoundError(detail="Zone type not found")


@router.patch(
    "/zone",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.Zone
)
async def update_zone(
        id: int,
        data: schemas.ZoneUpdate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    zone = await crud.zone.get(db=db, id=id)
    if zone is None:
        raise NotFoundError("Zone not found")
    try:
        return await crud.zone.update(db=db, db_obj=zone, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.patch(
    "/zone/type",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.ZoneType
)
async def update_zone_type(
        id: int,
        data: schemas.ZoneTypeCreate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    zone_type = await crud.zone_type.get(db=db, id=id)
    if zone_type is None:
        raise NotFoundError("Zone type not found")
    return await crud.zone_type.update(db=db, db_obj=zone_type, obj_in=data)
