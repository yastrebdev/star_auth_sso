from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user import User
from services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="EmailAuth"
)


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    return AuthService.decode_token(token)


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db)
) -> User:
    email: str = payload.get("sub")
    return await AuthService.get_user_by_email(db, email)


def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user)
) -> User:
    return AuthService.validate_user_active(user)


async def validate_auth_user(
    username: EmailStr | str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db)
) -> User:
    return await AuthService.authenticate_user(db, username, password)