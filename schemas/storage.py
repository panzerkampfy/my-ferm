from typing import Optional
from schemas import APIModel


class StorageCreate(APIModel):
    name: str
    count: int


class Storage(StorageCreate):
    id: int


class StorageUpdate(APIModel):
    name: Optional[str]
    count: Optional[int]

