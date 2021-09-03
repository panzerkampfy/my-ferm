from typing import Optional
from schemas import APIModel


class ProductCreate(APIModel):
    type_id: int
    title: str
    grade: Optional[str]
    count: int


class Product(ProductCreate):
    id: int


class ProductUpdate(APIModel):
    type_id: Optional[int]
    title: Optional[str]
    grade: Optional[str]
    count: Optional[int]

