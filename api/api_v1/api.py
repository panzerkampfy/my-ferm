from fastapi import APIRouter
from api.api_v1.endpoints import login

router = APIRouter()
router.include_router(login.router, prefix="/login", tags=["login"])
