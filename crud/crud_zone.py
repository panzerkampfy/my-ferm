from typing import List, Optional

from sqlalchemy.orm import Session

import crud
from crud.base import CRUDBase
from models import Zone, ZoneType
from schemas import ZoneCreate, ZoneTypeCreate


class CRUDZone(CRUDBase[Zone, ZoneCreate, None]):
    async def get_list(self, db: Session,
                       user_id: Optional[int] = None,
                       type_id: Optional[int] = None
    ) -> List[Zone]:
        if user_id and type_id:
            return db.query(self.model).filter(self.model.user_id == user_id, self.model.type_id == type_id).all()
        if type_id:
            return db.query(self.model).filter(self.model.type_id == type_id).all()
        if user_id:
            return db.query(self.model).filter(self.model.user_id == user_id).all()
        return await crud.zone.get_multi(db)
            

zone = CRUDZone(Zone)


class CRUDZoneType(CRUDBase[ZoneType, ZoneTypeCreate, None]):
    pass


zone_type = CRUDZoneType(ZoneType)
