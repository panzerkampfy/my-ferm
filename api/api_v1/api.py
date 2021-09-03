from fastapi import APIRouter
from api.api_v1.endpoints import login, users, roles, zones, storage, products, jobs, storage_job, product_zone

router = APIRouter()
router.include_router(login.router, tags=["login"])
router.include_router(roles.router, tags=["roles"])
router.include_router(users.router, tags=["users"])
router.include_router(zones.router, tags=["zones"])
router.include_router(storage.router, tags=["storage"])
router.include_router(products.router, tags=["products"])
router.include_router(jobs.router, tags=["jobs"])
router.include_router(storage_job.router, tags=["storage job"])
router.include_router(product_zone.router, tags=["product zone"])
