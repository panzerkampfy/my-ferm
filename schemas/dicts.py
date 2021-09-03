from schemas.base import APIModel
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class DictionaryBase(APIModel):
    id: int
    name: str


