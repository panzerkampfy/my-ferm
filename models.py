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
    jobs = relationship("Job", back_populates="users")
    zones = relationship("Zone", back_populates="users")
    role = relationship("Role", back_populates="users")


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


class ProductZone(Base):
    __tablename__ = "product_zone"

    product_id = Column(INTEGER, ForeignKey("products.id", ondelete="CASCADE"))
    zone_id = Column(INTEGER, ForeignKey("zones.id", ondelete="CASCADE"))
    count = Column(INTEGER, nullable=False)

    zone = relationship("Zone", back_populates="product_zones")
    product = relationship("Product", back_populates="product_zones")
    jobs = relationship("Job", back_populates="product_zones")


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
    product_zones = relationship("ProductZone", back_populates="product")


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
    product_zone_id = Column(INTEGER, ForeignKey("product_zone.id"), nullable=True)

    type = relationship("JobType", back_populates="jobs")
    storage_jobs = relationship("StorageJob", back_populates="jobs")
    users = relationship("User", back_populates="jobs")
    product_zones = relationship("ProductZone", back_populates="jobs")


class Storage(Base):
    __tablename__ = "storage"

    name = Column(String, nullable=False)
    count = Column(INTEGER, nullable=False)

    storage_jobs = relationship("StorageJob", back_populates="storages")


class StorageJob(Base):
    __tablename__ = "storage_jobs"

    storage_id = Column(INTEGER, ForeignKey("storage.id", ondelete="CASCADE"))
    job_id = Column(INTEGER, ForeignKey("jobs.id", ondelete="CASCADE"))
    count = Column(INTEGER, nullable=True)

    jobs = relationship("Job", back_populates="storage_jobs")
    storages = relationship("Storage", back_populates="storage_jobs")
