import pytest


class TestStorageJob:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_users_update(self,
                          user_factory,
                          token_headers_factory,
                          ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "login": "string",
            "firstName": "string",
            "middleName": "string",
            "lastName": "string",
            "roleId": 2
        }
        response = self.client.patch(
            "/api/v1/user?id=" + str(worker.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_user_update_wrong_data(self,
                                    user_factory,
                                    token_headers_factory,
                                    ):
        password = "test"
        user = user_factory(password=password, role_id=2)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "login": "string",
            "firstName": "string",
            "middleName": "string",
            "lastName": "string",
            "roleId": 1303
        }
        response = self.client.patch(
            "/api/v1/user?id=" + str(worker.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 400
