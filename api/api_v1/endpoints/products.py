import re
from typing import Any, List
from fastapi import APIRouter, Depends
from pydantic import ValidationError
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
    "/product",
    response_model=schemas.Product,
    status_code=201
)
async def create_product(
        create_data: schemas.ProductCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    # return await crud.product.create(db, obj_in=create_data)
    try:
        return await crud.product.create(db, obj_in=create_data)
    except ValidationError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.post(
    "/product/type",
    response_model=schemas.ProductType,
    status_code=201
)
async def create_product_type(
        create_data: schemas.ProductTypeCreate,
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    # return await crud.product_type.create(db, obj_in=create_data)
    try:
        return await crud.product_type.create(db, obj_in=create_data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.get(
    "/products",
    response_model=List[schemas.Product]
)
async def get_products(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    products = await crud.product.get_multi(db)
    return products


@router.get(
    "/zone/types",
    response_model=List[schemas.ProductType]
)
async def get_product_types(
        db: Session = Depends(deps.get_db),
        manager: models.User = Depends(deps.get_current_manager_user),
) -> Any:
    product_types = await crud.product_type.get_multi(db)
    return product_types


@router.delete(
    "/product",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Product not found"},
    },
)
async def delete_product(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    try:
        await crud.product.remove(db=db, id=id)
    except:
        raise NotFoundError(detail="Product not found")


@router.delete(
    "/product/type",
    status_code=204,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Product type not found"},
    },
)
async def delete_product_types(
        id: int,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    try:
        await crud.product_type.remove(db=db, id=id)
    except:
        raise NotFoundError(detail="Product not found")


@router.patch(
    "/product",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Product not found"},
    },
    response_model=schemas.Product
)
async def update_product(
        id: int,
        data: schemas.ProductUpdate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    product = await crud.product.get(db=db, id=id)
    if product is None:
        raise NotFoundError("Product not found")
    try:
        return await crud.product.update(db=db, db_obj=product, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)


@router.patch(
    "/product/type",
    status_code=200,
    responses={
        403: {"model": schemas.GenericHTTPError, "description": "Permission denied"},
        404: {"model": schemas.GenericHTTPError, "description": "Product zone not found"},
    },
    response_model=schemas.ProductType
)
async def update_product_type(
        id: int,
        data: schemas.ProductTypeCreate,
        manager: models.User = Depends(deps.get_current_manager_user),
        db: Session = Depends(deps.get_db)
) -> Any:
    product_type = await crud.product_type.get(db=db, id=id)
    if product_type is None:
        raise NotFoundError("Zone not found")
    try:
        return await crud.product_type.update(db=db, db_obj=product_type, obj_in=data)
    except IntegrityError as exc:
        match_exec = re.search(r"\((.*?)\)\=\((.*?)\)", str(exc))
        message: str = f"Not found {match_exec.group(1)}" if match_exec else ""
        raise NotFoundError(message)
