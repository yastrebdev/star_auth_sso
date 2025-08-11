from fastapi import APIRouter

from .endpoints import auth

router = APIRouter(prefix="/v1")

router.include_router(auth.router, prefix="/auth", tags=["Users"])