from typing import Generator

import pytest
from fastapi.testclient import TestClient
from api import deps
from db.session import SessionLocal, engine
from core.main import app
from . import factories


@pytest.fixture(scope="session")
def db_session():
    SessionLocal.configure(bind=engine)
    yield SessionLocal


@pytest.fixture(scope="function")
def db(db_session) -> Generator:
    session = db_session()
    try:
        session.begin(subtransactions=True)
        app.dependency_overrides[deps.get_db] = lambda: session
        yield session
    finally:
        session.rollback()
        app.dependency_overrides = {}
    db_session.remove()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture()
def role_factory():
    return factories.RoleFactory


@pytest.fixture()
def user_factory():
    return factories.UserFactory


@pytest.fixture()
def token_factory(client: TestClient):
    return factories.TokenFactory(client)


@pytest.fixture()
def token_headers_factory(client: TestClient):
    return factories.TokenHeadersFactory(client)


@pytest.fixture()
def product_factory():
    return factories.ProductFactory


@pytest.fixture()
def product_type_factory():
    return factories.ProductTypeFactory


def zone_factory():
    return factories.ZoneFactory


@pytest.fixture()
def zone_type_factory():
    return factories.ZoneTypeFactory


@pytest.fixture()
def job_factory():
    return factories.JobFactory


@pytest.fixture()
def job_type_factory():
    return factories.JobTypeFactory
