import pytest


class TestZone:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_product_create(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        data = {
          "typeId": 1,
          "title": "string",
          "grade": "string",
          "count": 3
        }
        response = self.client.post(
            "/api/v1/product",
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_create_wrong_credentials(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "typeId": 1,
            "title": "string",
            "grade": "string",
            "count": 3
        }
        response = self.client.post(
            "/api/v1/product",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_product_update(self, user_factory, token_headers_factory, product_factory, product_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        data = {
            "count": 10
        }
        response = self.client.patch(
            "/api/v1/product?id=" + str(product.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_update_wrong_data(self, user_factory, token_headers_factory, product_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "typeId": 10
        }
        product = product_factory()
        response = self.client.patch(
            "/api/v1/product?id=" + str(product.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 400

    def test_product_delete(self, user_factory, token_headers_factory, product_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        product = product_factory()
        response = self.client.delete(
            "/api/v1/product?id=" + str(product.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_product_delete_wrong_id(self, user_factory, token_headers_factory, product_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        product = product_factory()
        response = self.client.delete(
            "/api/v1/product?id=" + str(product.id + 10),
            headers=headers
        )
        assert response.status_code == 400


# --------------------------------------------------


class TestProductType:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_product_type_create(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        data = {
          "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/product/type",
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_type_create_wrong_credentials(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/product/type",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_product_type_update(self, user_factory, token_headers_factory, product_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        product_type = product_type_factory()
        data = {
            "name": "тест мессагес",
        }
        response = self.client.patch(
            "/api/v1/product/type?id=" + str(product_type.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_type_delete(self, user_factory, token_headers_factory, product_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        product_type = product_type_factory()
        response = self.client.delete(
            "/api/v1/product/type?id=" + str(product_type.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_product_type_delete_wrong_id(self, user_factory, token_headers_factory, product_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        product_type = product_type_factory()
        response = self.client.delete(
            "/api/v1/product/type?id=" + str(product_type.id + 10),
            headers=headers
        )
        assert response.status_code == 400
