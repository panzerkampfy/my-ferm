from typing import Optional

from schemas import APIModel


class TypesBase(APIModel):
    id: int
    name: str


class TypesCreateBase(APIModel):
    name: str


class Role(TypesBase):
    pass


class RoleCreate(TypesCreateBase):
    pass


class ProductType(TypesBase):
    pass


class ProductTypeCreate(TypesCreateBase):
    pass
