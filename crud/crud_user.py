from typing import Optional

from fastapi.encoders import jsonable_encoder
from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models import Role, User
from schemas import UserCreate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, None]):
    async def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).join(Role).filter(User.email == email).first()

    async def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def is_admin_user(self, user: User):
        return user.role.slug == "admin"

    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        obj_in_data["hashed_password"] = get_password_hash(obj_in_data.pop("password"))
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
