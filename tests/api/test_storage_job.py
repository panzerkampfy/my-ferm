import pytest


class TestStorageJob:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        self.client = client
        self.db = db

    def test_storage_job_create(self,
                                user_factory,
                                token_headers_factory,
                                product_factory,
                                zone_factory,
                                product_type_factory,
                                zone_type_factory,
                                storage_factory,
                                job_type_factory,
                                product_zone_factory,
                                job_factory
                                ):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        worker = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)

        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job_type = job_type_factory()
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        storage = storage_factory()

        data = {
            "storageId": storage.id,
            "jobId": job.id,
            "count": 10
        }
        response = self.client.post(
            "/api/v1/storage_job",
            json=data,
            headers=headers
        )
        assert response.status_code == 201

    def test_storage_job_update(self,
                                user_factory,
                                token_headers_factory,
                                product_type_factory,
                                zone_type_factory,
                                product_factory,
                                zone_factory,
                                product_zone_factory,
                                job_type_factory,
                                job_factory,
                                storage_factory,
                                storage_job_factory
                                ):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        worker = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        storage = storage_factory()
        storage_job = storage_job_factory(storage_id=storage.id, job_id=job.id)

        data = {
            "count": 100
        }
        response = self.client.patch(
            "/api/v1/storage_job?id=" + str(storage_job.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 200

    def test_storage_job_update_wrong_data(self,
                                           user_factory,
                                           token_headers_factory,
                                           product_factory,
                                           zone_factory,
                                           product_type_factory,
                                           zone_type_factory,
                                           product_zone_factory,
                                           job_type_factory,
                                           job_factory,
                                           storage_factory,
                                           storage_job_factory
                                           ):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        worker = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        storage = storage_factory()
        storage_job = storage_job_factory(storage_id=storage.id, job_id=job.id)

        data = {
            "storage_id": storage.id + 10,
            "count": 100
        }
        response = self.client.patch(
            "/api/v1/storage_job?id=" + str(storage_job.id),
            json=data,
            headers=headers
        )
        assert response.status_code == 400

    def test_storage_job_delete(self,
                                user_factory,
                                token_headers_factory,
                                product_factory,
                                zone_factory,
                                product_type_factory,
                                zone_type_factory,
                                product_zone_factory,
                                job_type_factory,
                                job_factory,
                                storage_factory,
                                storage_job_factory
                                ):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        worker = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        storage = storage_factory()
        storage_job = storage_job_factory(storage_id=storage.id, job_id=job.id)

        response = self.client.delete(
            "/api/v1/storage_job?id=" + str(storage_job.id),
            headers=headers
        )
        assert response.status_code == 204

    def test_storage_job_delete_wrong_id(self,
                                         user_factory,
                                         token_headers_factory,
                                         product_factory,
                                         zone_factory,
                                         product_type_factory,
                                         zone_type_factory,
                                         product_zone_factory,
                                         job_type_factory,
                                         job_factory,
                                         storage_factory,
                                         storage_job_factory
                                         ):
        password = "test"
        user = user_factory(password=password, role_name="Администратор")
        worker = user_factory(login="worker", password=password, role_name="Работник")
        headers = token_headers_factory.create(user.login, password)

        job_type = job_type_factory()
        product_type = product_type_factory()
        product = product_factory(type_id=product_type.id)
        zone_type = zone_type_factory()
        zone = zone_factory(type_id=zone_type.id)
        product_zone = product_zone_factory(product_id=product.id, zone_id=zone.id)
        job = job_factory(type_id=job_type.id, user_id=worker.id, product_zone_id=product_zone.id)
        storage = storage_factory()
        storage_job = storage_job_factory(storage_id=storage.id, job_id=job.id)

        response = self.client.delete(
            "/api/v1/storage_job?id=" + str(storage_job.id + 10),
            headers=headers
        )
        assert response.status_code == 400
