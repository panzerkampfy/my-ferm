import pytest


class TestAuth:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_token_login(self, user_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        response = self.client.post(
            "/api/v1/token",
            json={"login": user.login, "password": password},
        )
        assert response.status_code == 200
        assert response.json()["accessToken"]

    def test_token_login_wrong_password(self):
        response = self.client.post(
            "/api/v1/token",
            json={"login": "ksjbdfkljwsvhebk", "password": "shdn2fkjbsdf12"},
        )
        assert response.status_code == 400
