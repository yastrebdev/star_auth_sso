from fastapi import APIRouter, Depends

from dependencies.auth import get_current_active_auth_user
from schemas.user import User

router = APIRouter()


@router.get("/user/me")
async def auth_user_check_self_info(
    user: User = Depends(get_current_active_auth_user),
):
    return {
        "username": user.username,
        "email": user.email
    }