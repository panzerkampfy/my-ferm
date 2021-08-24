import pytest


class TestStorage:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_storage_create(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        data = {
          "name": "string",
          "count": 10
        }
        response = self.client.post(
            "/api/v1/storage",
            json=data,
            headers=headers
        )
        assert response.status_code == 201

    def test_storage_create_wrong_credentials(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "name": "string",
            "count": 10
        }
        response = self.client.post(
            "/api/v1/storage",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_storage_update(self, user_factory, token_headers_factory, storage_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "name": "string",
            "count": 10
        }
        storage = storage_factory()
        response = self.client.patch(
            "/api/v1/storage?id=" + str(storage.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_zone_delete(self, user_factory, token_headers_factory, storage_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        storage = storage_factory()
        response = self.client.delete(
            "/api/v1/storage?id=" + str(storage.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_zone_delete_wrong_id(self, user_factory, token_headers_factory, storage_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        storage = storage_factory()
        response = self.client.delete(
            "/api/v1/storage?id=" + str(storage.id + 10),
            headers=headers
        )
        assert response.status_code == 400
