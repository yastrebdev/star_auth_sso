from fastapi import APIRouter, Depends, HTTPException, status, Form
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import encode_jwt, verify_password
from database import get_db
from schemas.token import Token
from schemas.user import UserCreate, UserRead, LoginUser
from crud.user import user_crud
from services.user_service import user_service

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await user_crud.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    user = await user_service.create_user(db, user_in)
    return user


async def validate_auth_user(
    email: EmailStr = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db)
):
    unauthed_exc = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password"
    )
    existing_user = await user_crud.get_by_email(db, email)
    if not existing_user:
        raise unauthed_exc

    if verify_password(
        plain_password=password,
        hashed_password=existing_user.hashed_password
    ):
        return existing_user
    raise unauthed_exc


@router.post("/login")
async def login_user(
    user: LoginUser = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.email
    }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token = token,
        token_type = "Bearer"
    )