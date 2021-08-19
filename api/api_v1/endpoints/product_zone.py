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
    "/product_zone",
    response_model=schemas.ProductZone,
)
async def create_product_zone(
        create_data: schemas.ProductZoneCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    # return await crud.product_zone.create(db, obj_in=create_data)
    try:
        return await crud.product_zone.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.get(
    "/product_zones",
    response_model=List[schemas.ProductZone]
)
async def get_product_zones(
        zone: Optional[int] = None,
        product: Optional[int] = None,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    # return await crud.product_zone.get_multi(db)
    return await crud.product_zone.get_list(db, zone_id=zone, product_id=product)


@router.delete(
    "/product_zone",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
)
async def delete_product_zone(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    try:
        await crud.product_zone.remove(db=db, id=id)
    except:
        raise NotFoundError(detail="Product zone not found")
    return Response(status_code=204)


@router.patch(
    "/product_zone",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
    },
    response_model=schemas.ProductZone
)
async def update_product(
        id: int,
        data: schemas.ProductZoneUpdate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    # product_zone = await crud.product_zone.get(db=db, id=id)
    # updated = await crud.product_zone.update(db=db, db_obj=product_zone, obj_in=data)
    # return updated
    product_zone = await crud.product_zone.get(db=db, id=id)
    if product_zone is None:
        raise NotFoundError("Product zone not found")
    try:
        return await crud.product_zone.update(db=db, db_obj=product_zone, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)
