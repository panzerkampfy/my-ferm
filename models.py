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
    zones = relationship("Zone", back_populates="users")


class ProductType(Base):
    __tablename__ = "product_types"

    name = Column(String, nullable=False, unique=True)
    products = relationship("Product", back_populates="product_type")


class Product(Base):
    __tablename__ = "products"

    title = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    count = Column(INTEGER, nullable=False)

    type_id = Column(INTEGER, ForeignKey("product_types.id", ondelete="CASCADE"))
    product_type = relationship("ProductType", back_populates="products")


class ZoneType(Base):
    __tablename__ = "zone_types"

    name = Column(String, nullable=False, unique=True)
    zones = relationship("Zone", back_populates="type")


class Zone(Base):
    __tablename__ = "zones"

    title = Column(String, nullable=False)
    capacity = Column(INTEGER, nullable=False)

    type_id = Column(INTEGER, ForeignKey("zone_types.id", ondelete="CASCADE"))
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"))

    product_zones = relationship("ProductZone", cascade="all, delete", passive_deletes=True)
    users = relationship("User", back_populates="zones")
    type = relationship("ZoneType", back_populates="zones")


class JobType(Base):
    __tablename__ = "job_types"

    name = Column(String, nullable=False, unique=True)

    jobs = relationship("Job", back_populates="type")


class Job(Base):
    __tablename__ = "jobs"

    title = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Ожидает выполнения")
    description = Column(String, nullable=True)
    count = Column(INTEGER, nullable=True)
    date = Column(DateTime, default=func.now())
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"))
    type_id = Column(INTEGER, ForeignKey("job_types.id", ondelete="CASCADE"))

    type = relationship("JobType", back_populates="jobs")
    users = relationship("User", back_populates="jobs")
