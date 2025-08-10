from fastapi import APIRouter

from .endpoints import users

router = APIRouter(prefix="/v1")

router.include_router(users.router, prefix="/users", tags=["Users"])