from db.base_class import Base  # noqa
from sqlalchemy import Column, Date, ForeignKey, String, INTEGER, DateTime, func
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"

    name = Column(String, nullable=False, unique=True)

    users = relationship(
        "User", back_populates="role", cascade="all, delete", passive_deletes=True
    )


class User(Base):
    __tablename__ = "users"

    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), onupdate=func.now())

    role_id = Column(INTEGER, ForeignKey("roles.id", ondelete="CASCADE"))
    jobs = relationship(
        "Job", back_populates="jobs", cascade="all, delete", passive_deletes=True
    )
    zones = relationship(
        "Zones", back_populates="zone", cascade="all, delete", passive_deletes=True
    )


class ZoneType(Base):
    __tablename__ = "zone_types"

    name = Column(String, nullable=False, unique=True)
    zones = relationship(
        "Zone", back_populates="zonetype", cascade="all, delete", passive_deletes=True
    )


class Zone(Base):
    __tablename__ = "zones"

    title = Column(String, nullable=False)
    capacity = Column(INTEGER, nullable=False)

    type_id = Column(INTEGER, ForeignKey("zone_types.id", ondelete="CASCADE"))
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"))

    product_zones = relationship(
        "Product_zone", back_populates="productzone", cascade="all, delete", passive_deletes=True
    )


class ProductZone(Base):
    __tablename__ = "product_zone"

    product_id = Column(INTEGER, ForeignKey("product.id", ondelete="CASCADE"))
    zone_id = Column(INTEGER, ForeignKey("zone.id", ondelete="CASCADE"))
    count = Column(INTEGER, nullable=False)
    jobs = relationship(
        "Jobs", back_populates="job", cascade="all, delete", passive_deletes=True
    )


class ProductType(Base):
    __tablename__ = "product_types"

    name = Column(String, nullable=False, unique=True)
    products = relationship(
        "Products", back_populates="producttype", cascade="all, delete", passive_deletes=True
    )


class Product(Base):
    __tablename__ = "products"

    title = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    count = Column(INTEGER, nullable=False)

    type_id = Column(INTEGER, ForeignKey("product_types.id", ondelete="CASCADE"))
    zones = relationship(
        "Zones", back_populates="zone", cascade="all, delete", passive_deletes=True
    )


class JobType(Base):
    __tablename__ = "job_types"

    name = Column(String, nullable=False, unique=True)
    jobs = relationship(
        "Jobs", back_populates="job", cascade="all, delete", passive_deletes=True
    )


class Job(Base):
    __tablename__ = "jobs"

    title = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Ожидает выполнения")
    description = Column(String, nullable=True)
    count = Column(INTEGER, nullable=True)
    date = Column(DateTime)
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"))
    type_id = Column(INTEGER, ForeignKey("job_types.id", ondelete="CASCADE"))

    storage_jobs = relationship(
        "Job", back_populates="jobtype", cascade="all, delete", passive_deletes=True
    )


class Storage(Base):
    __tablename__ = "storage"

    name = Column(String, nullable=False)
    count = Column(INTEGER, nullable=False)
    storage_jobs = relationship(
        "Storage_jobs", back_populates="storagejob", cascade="all, delete", passive_deletes=True
    )


class StorageJob(Base):
    __tablename__ = "storage_jobs"

    storage_id = Column(INTEGER, ForeignKey("storage.id", ondelete="CASCADE"))
    job_id = Column(INTEGER, ForeignKey("job.id", ondelete="CASCADE"))
    count = Column(INTEGER, nullable=True)
