import pytest


class TestProductZone:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_product_zone_create(self,
                        user_factory,
                        token_headers_factory,
                        product_factory,
                        zone_factory,
                        product_type_factory,
                        zone_type_factory,
                        ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=worker.id)

        data = {
          "productId": product.id,
          "zoneId": zone.id,
          "count": 10
        }
        response = self.client.post(
            "/api/v1/product_zone",
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_zone_update(self,
                        user_factory,
                        token_headers_factory,
                        product_type_factory,
                        zone_type_factory,
                        product_factory,
                        zone_factory,
                        product_zone_factory
                        ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=worker.id)
        product_zone = product_zone_factory(zone_id=zone.id, product_id=product.id)

        data = {
            "count": 100
        }
        response = self.client.patch(
            "/api/v1/product_zone?id=" + str(product_zone.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_zone_update_wrong_data(self,
                                   user_factory,
                                   token_headers_factory,
                                   product_factory,
                                   zone_factory,
                                   product_type_factory,
                                   zone_type_factory,
                                   product_zone_factory,

                                   ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=worker.id)
        product_zone = product_zone_factory(zone_id=zone.id, product_id=product.id)

        data = {
            "zoneId": zone.id + 10,
        }
        response = self.client.patch(
            "/api/v1/product_zone?id=" + str(product_zone.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 400

    def test_product_zone_delete(self,
                        user_factory,
                        token_headers_factory,
                        product_factory,
                        zone_factory,
                        product_type_factory,
                        zone_type_factory,
                        product_zone_factory,
                        ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=worker.id)
        product_zone = product_zone_factory(zone_id=zone.id, product_id=product.id)

        response = self.client.delete(
            "/api/v1/product_zone?id=" + str(product_zone.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_product_zone_delete_wrong_id(self,
                                 user_factory,
                                 token_headers_factory,
                                 product_factory,
                                 zone_factory,
                                 product_type_factory,
                                 zone_type_factory,
                                 product_zone_factory,
                                 ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=worker.id)
        product_zone = product_zone_factory(zone_id=zone.id, product_id=product.id)

        response = self.client.delete(
            "/api/v1/product_zone?id=" + str(product_zone.id + 10),
            headers=headers
        )
        assert response.status_code == 400
