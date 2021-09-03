from typing import Optional

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Role


class CRUDRole(CRUDBase[Role, None, None]):
    async def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(self.model).filter(self.model.name == name).first()


role = CRUDRole(Role)
