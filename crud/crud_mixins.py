from typing import Generic, Type, TypeVar

import crud
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class CheckUserIdMixin(Generic[ModelType]):
    def __init__(self, type: Type[ModelType]):
        self.type = type

    async def check_type_id(self, db: Session, id: int) -> bool:
        if await crud.zone_type.get(db, id=id):
            return True
        return False


class CheckTypeIdMixin(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def check_type_id(self, db: Session, id: int) -> bool:
        if await crud.zone_type.get(db, id=id):
            return True
        return False