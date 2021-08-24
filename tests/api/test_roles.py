import pytest


class TestRole:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_get_roles(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        response = self.client.get(
            "/api/v1/roles",
            headers=headers
        )
        assert response.status_code == 200

    def test_role_create(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        data = {
          "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/role",
            json=data,
            headers=headers
        )
        assert response.status_code == 201

    def test_role_create_wrong_credentials(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)
        data = {
            "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/role",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_role_update(self, user_factory, token_headers_factory, role_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        job_type = role_factory()
        data = {
            "name": "тест мессагес",
        }
        response = self.client.patch(
            "/api/v1/role?id=" + str(job_type.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_role_delete(self, user_factory, token_headers_factory, role_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        job_type = role_factory()
        response = self.client.delete(
            "/api/v1/role?id=" + str(job_type.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_role_delete_wrong_id(self, user_factory, token_headers_factory, role_factory):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        headers = token_headers_factory.create(user.login, password)
        job_type = role_factory()
        response = self.client.delete(
            "/api/v1/role?id=" + str(job_type.id + 10),
            headers=headers
        )
        assert response.status_code == 400
