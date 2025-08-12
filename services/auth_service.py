from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_jwt, verify_password
from schemas.user import User
from crud.user import user_crud


class AuthService:
    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return decode_jwt(token)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token error"
            )

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User:
        user = await user_crud.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalid"
            )
        return user

    @staticmethod
    def validate_user_active(user: User) -> User:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user inactive"
            )
        return user

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: EmailStr | str, password: str) -> User:
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password"
        )

        existing_user = await user_crud.get_by_username(db, username)
        if not existing_user:
            raise unauthed_exc

        if not verify_password(
                plain_password=password,
                hashed_password=existing_user.hashed_password
        ):
            raise unauthed_exc

        return existing_user