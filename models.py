from db.base_class import Base  # noqa
from sqlalchemy import Column, ForeignKey, String, INTEGER, DateTime, func
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True), default=None)

    role_id = Column(INTEGER, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

