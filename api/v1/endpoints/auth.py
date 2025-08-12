from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import encode_jwt
from database import get_db
from dependencies.auth import validate_auth_user
from schemas.token import Token
from schemas.user import UserCreate, UserRead, LoginUser
from crud.user import user_crud
from services.user_service import create_user as create

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_user = await user_crud.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    user = await create(db, user_in)
    return user


@router.post("/login")
async def login_user(
    user: LoginUser = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.username
    }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token = token,
        token_type = "Bearer"
    )