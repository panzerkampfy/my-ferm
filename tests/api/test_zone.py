import pytest


class TestZone:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_zone_create(self, user_factory, token_headers_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        data = {
          "typeId": zone_type.id,
          "title": "тест мессагес",
          "capacity": 10,
          "userId": user.id
        }
        response = self.client.post(
            "/api/v1/zone",
            json=data,
            headers=headers
        )
        assert response.status_code == 201

    def test_zone_create_wrong_data(self, user_factory, token_headers_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        data = {
          "typeId": zone_type.id,
          "title": "тест мессагес",
          "capacity": 10,
          "userId": 2214124
        }
        response = self.client.post(
            "/api/v1/zone",
            json=data,
            headers=headers
        )
        assert response.status_code == 400

    def test_zone_create_wrong_credentials(self, user_factory, token_headers_factory, zone_type_factory):
        password = "test"
        user = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        data = {
          "typeId": zone_type.id,
          "title": "тест мессагес",
          "capacity": 10,
          "userId": user.id
        }
        response = self.client.post(
            "/api/v1/zone",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_zone_update(self, user_factory, token_headers_factory, zone_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        data = {
          "title": "вhhhhhhh",
          "capacity": 100,
        }
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=user.id)
        response = self.client.patch(
            "/api/v1/zone?id=" + str(zone.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_zone_update_wrong_data(self, user_factory, token_headers_factory, zone_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")

        headers = token_headers_factory.create(user.login, password)
        data = {
          "typeId": 121312331,
        }
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=user.id)
        response = self.client.patch(
            "/api/v1/zone?id=" + str(zone.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 400

    def test_zone_delete(self, user_factory, token_headers_factory, zone_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=user.id)
        response = self.client.delete(
            "/api/v1/zone?id=" + str(zone.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_zone_delete_wrong_id(self, user_factory, token_headers_factory, zone_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=user.id)
        response = self.client.delete(
            "/api/v1/zone?id=" + str(zone.id + 10),
            headers=headers
        )
        assert response.status_code == 400


# --------------------------------------------------


class TestZoneType:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_zone_type_create(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        data = {
          "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/zone/type",
            json=data,
            headers=headers
        )
        assert response.status_code == 201

    def test_zone_type_create_wrong_credentials(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)
        data = {
            "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/zone/type",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_zone_type_update(self, user_factory, token_headers_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        data = {
            "name": "тест мессагес",
        }
        response = self.client.patch(
            "/api/v1/zone/type?id=" + str(zone_type.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_zone_type_delete(self, user_factory, token_headers_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        response = self.client.delete(
            "/api/v1/zone/type?id=" + str(zone_type.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_zone_type_delete_wrong_id(self, user_factory, token_headers_factory, zone_type_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        zone_type = zone_type_factory()
        response = self.client.delete(
            "/api/v1/zone/type?id=" + str(zone_type.id + 10),
            headers=headers
        )
        assert response.status_code == 400