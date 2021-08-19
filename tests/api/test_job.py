import pytest


class TestJob:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_job_create(self,
                        user_factory,
                        token_headers_factory,
                        job_type_factory,
                        product_factory,
                        zone_factory,
                        product_type_factory,
                        zone_type_factory,
                        product_zone_factory
                        ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id, user_id=worker.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)

        data = {
            "typeId": job_type.id,
            "title": "string",
            "description": "string",
            "userId": worker.id,
            "productZoneId": product_zone.id
        }
        response = self.client.post(
            "/api/v1/job",
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_job_update(self,
                        user_factory,
                        token_headers_factory,
                        job_type_factory,
                        product_factory,
                        zone_factory,
                        product_type_factory,
                        zone_type_factory,
                        product_zone_factory,
                        job_factory
                        ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        worker = user_factory(login="worker", password=password, role_id=3)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)

        data = {
            "description": "stringgfgdfsdff",
            "userId": worker.id,
        }
        response = self.client.patch(
            "/api/v1/job?id=" + str(job.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_job_update_wrong_data(self,
                                   user_factory,
                                   token_headers_factory,
                                   job_type_factory,
                                   product_factory,
                                   zone_factory,
                                   product_type_factory,
                                   zone_type_factory,
                                   product_zone_factory,
                                   job_factory
                                   ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        worker = user_factory(login="worker", password=password, role_id=3)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job_type = job_type_factory()
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)

        data = {
            "description": "stringgfgdfsdff",
            "userId": worker.id + 10,
        }
        response = self.client.patch(
            "/api/v1/job?id=" + str(job.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 400

    def test_job_delete(self,
                        user_factory,
                        token_headers_factory,
                        job_type_factory,
                        product_factory,
                        zone_factory,
                        product_type_factory,
                        zone_type_factory,
                        product_zone_factory,
                        job_factory
                        ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        response = self.client.delete(
            "/api/v1/job?id=" + str(job.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_job_delete_wrong_id(self,
                                 user_factory,
                                 token_headers_factory,
                                 job_type_factory,
                                 product_factory,
                                 zone_factory,
                                 product_type_factory,
                                 zone_type_factory,
                                 product_zone_factory,
                                 job_factory
                                 ):
        password = "test"
        user = user_factory(password=password, role_id=1)
        worker = user_factory(login="worker", password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        response = self.client.delete(
            "/api/v1/job?id=" + str(job.id + 10),
            headers=headers
        )
        assert response.status_code == 400


# --------------------------------------------------


class TestJobType:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_job_type_create(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        data = {
          "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/job/type",
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_job_type_create_wrong_credentials(self, user_factory, token_headers_factory):
        password = "test"
        user = user_factory(password=password, role_id=3)
        headers = token_headers_factory.create(user.login, password)
        data = {
            "name": "тест мессагес",
        }
        response = self.client.post(
            "/api/v1/job/type",
            json=data,
            headers=headers
        )
        assert response.status_code == 403

    def test_job_type_update(self, user_factory, token_headers_factory, job_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        job_type = job_type_factory()
        data = {
            "name": "тест мессагес",
        }
        response = self.client.patch(
            "/api/v1/job/type?id=" + str(job_type.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_product_type_delete(self, user_factory, token_headers_factory, job_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        job_type = job_type_factory()
        response = self.client.delete(
            "/api/v1/job/type?id=" + str(job_type.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_product_type_delete_wrong_id(self, user_factory, token_headers_factory, job_type_factory):
        password = "test"
        user = user_factory(password=password, role_id=1)
        headers = token_headers_factory.create(user.login, password)
        job_type = job_type_factory()
        response = self.client.delete(
            "/api/v1/job/type?id=" + str(job_type.id + 10),
            headers=headers
        )
        assert response.status_code == 400
