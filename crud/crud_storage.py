from crud.base import CRUDBase
from models import Storage
from schemas import StorageCreate


class CRUDStorage(CRUDBase[Storage, StorageCreate, None]):
    pass


storage = CRUDStorage(Storage)

