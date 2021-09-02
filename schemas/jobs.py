from datetime import datetime
from typing import Optional
from schemas import APIModel


class JobCreate(APIModel):
    type_id: int
    title: str
    description: Optional[str]
    user_id: int
    product_zone_id: Optional[int]


class Job(JobCreate):
    id: int
    status: str
    date: datetime


class JobUpdate(APIModel):
    type_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    user_id: Optional[int]
    product_zone_id: Optional[int]

