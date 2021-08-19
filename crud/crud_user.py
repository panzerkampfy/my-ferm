from typing import Optional, List

import transliterate
from fastapi.encoders import jsonable_encoder
from core.security import get_password_hash, verify_password, generate_password
from crud.base import CRUDBase
from models import Role, User
from schemas import UserCreate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, None]):
    async def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).join(Role).filter(User.login == username).first()

    async def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def is_admin_user(self, user: User):
        return user.role_id == 1

    async def is_manager_user(self, user: User):
        if user.role_id == 2:
            return True
        else:
            return await self.is_admin_user(user=user)

    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        login = obj_in_data['last_name'] + obj_in_data['first_name'][0] + obj_in_data['middle_name'][0]
        obj_in_data['login'] = transliterate.translit(login.lower(), reversed=True)
        obj_in_data['password'] = generate_password()
        db_obj = User(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get_by_role(
        self, db: Session, *, role: int
    ) -> List[User]:
        return db.query(self.model).filter(User.role_id == role).all()


user = CRUDUser(User)
