from fastapi import APIRouter
from api.api_v1.endpoints import login, users, roles, products

router = APIRouter()
router.include_router(login.router, tags=["login"])
router.include_router(roles.router, tags=["roles"])
router.include_router(users.router, tags=["users"])
router.include_router(products.router, tags=["products"])\
