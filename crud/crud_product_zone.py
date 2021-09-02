from typing import Optional, List

from sqlalchemy.orm import Session

import crud
from crud.base import CRUDBase
from models import ProductZone
from schemas import ProductZoneCreate


class CRUDProductZone(CRUDBase[ProductZone, ProductZoneCreate, None]):
    async def get_list(self, db: Session,
                       product_id: Optional[int] = None,
                       zone_id: Optional[int] = None
    ) -> List[ProductZone]:
        if product_id and zone_id:
            return db.query(self.model).filter(self.model.product_id == product_id, self.model.type_id == zone_id).all()
        if zone_id:
            return db.query(self.model).filter(self.model.zone_id == zone_id).all()
        if product_id:
            return db.query(self.model).filter(self.model.product_id == product_id).all()
        return await crud.product_zone.get_multi(db)


product_zone = CRUDProductZone(ProductZone)

