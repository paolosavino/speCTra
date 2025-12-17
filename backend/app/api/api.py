from fastapi import APIRouter
from app.api.endpoints import gateway, api_keys

api_router = APIRouter()
api_router.include_router(gateway.router, prefix="/v1", tags=["gateway"])
api_router.include_router(api_keys.router, prefix="/v1", tags=["api_keys"])
