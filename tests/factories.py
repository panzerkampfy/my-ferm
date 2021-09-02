import factory
import models
from db import session


class BaseMeta:
    sqlalchemy_session = session.SessionLocal
    sqlalchemy_session_persistence = "flush"


class BaseType(factory.alchemy.SQLAlchemyModelFactory):
    name = "test messages"


class RoleFactory(BaseType, factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.Role


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.User

    first_name = "пользователь"
    middle_name = "пользователь"
    last_name = "пользователь"
    login = factory.Sequence(lambda n: "test-user-%d" % n)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return super()._create(model_class, *args, **kwargs)

    @factory.post_generation
    def role_name(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.role = (
                UserFactory._meta.sqlalchemy_session.query(models.Role)
                    .filter(models.Role.name == extracted)
                    .one()
            )
            UserFactory._meta.sqlalchemy_session.flush()


class TokenFactory:
    def __init__(self, client):
        self.client = client

    def create(self, login: str, password: str):
        login_data = {
            "login": login,
            "password": password,
        }
        response = self.client.post(
            "/api/v1/token", json=login_data
        )
        token = response.json()["accessToken"]
        return token


class TokenHeadersFactory(TokenFactory):
    def create(self, login: str, password: str):
        token = super().create(login, password)
        return {"Authorization": f"Bearer {token}"}


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.Product

    title = "test messages"
    grade = "test"
    count = 10


class ProductTypeFactory(BaseType, factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.ProductType

class ZoneFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.Zone

    title = "test messages"
    capacity = 10


class ZoneTypeFactory(BaseType, factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.ZoneType
