from typing import Optional
from uuid import UUID

from schemas.base import APIModel
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class DictionaryBase(APIModel):
    id: UUID
    name: str
    description: Optional[str]
    slug: Optional[str]


class Role(DictionaryBase):
    pass


class Gender(DictionaryBase):
    pass


class Subject(DictionaryBase):
    pass


class City(DictionaryBase):
    pass


class Category(DictionaryBase):
    pass
