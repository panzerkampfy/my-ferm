from typing import Optional
from schemas import APIModel


class ZoneCreate(APIModel):
    type_id: int
    title: str
    capacity: int
    user_id: Optional[int]


class Zone(ZoneCreate):
    id: int


class ZoneUpdate(APIModel):
    type_id: Optional[int]
    title: Optional[str]
    capacity: Optional[int]
    user_id: Optional[int]

