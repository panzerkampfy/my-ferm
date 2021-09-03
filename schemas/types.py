from typing import Optional

from schemas import APIModel


class TypesBase(APIModel):
    id: int
    name: str


class TypesCreateBase(APIModel):
    name: str


class Role(TypesBase):
    pass


class ZoneType(TypesBase):
    pass


class JobType(TypesBase):
    pass


class ProductType(TypesBase):
    pass


class RoleCreate(TypesCreateBase):
    pass


class ZoneTypeCreate(TypesCreateBase):
    pass


class JobTypeCreate(TypesCreateBase):
    pass


class ProductTypeCreate(TypesCreateBase):
    pass
