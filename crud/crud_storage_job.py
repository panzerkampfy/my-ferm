from crud.base import CRUDBase
from models import StorageJob
from schemas import StorageJobCreate


class CRUDStorageJob(CRUDBase[StorageJob, StorageJobCreate, None]):
    pass


storage_job = CRUDStorageJob(StorageJob)

