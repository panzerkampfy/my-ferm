from crud.base import CRUDBase
from models import Role, ZoneType, ProductType, JobType


class CRUDRole(CRUDBase[Role, None, None]):
    pass


class CRUDZoneType(CRUDBase[ZoneType, None, None]):
    pass


class CRUDProductType(CRUDBase[ProductType, None, None]):
    pass


class CRUDJobType(CRUDBase[JobType, None, None]):
    pass
