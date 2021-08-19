from typing import Optional
from schemas import APIModel


class StorageJobCreate(APIModel):
    storage_id: int
    job_id: int
    count: int


class StorageJob(StorageJobCreate):
    id: int


class StorageJobUpdate(APIModel):
    storage_id: Optional[int]
    job_id: Optional[int]
    count: Optional[int]

