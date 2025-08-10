from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import user_crud
from schemas.user import UserCreate
from core.security import hash_password

class UserService:
    async def create_user(self, session: AsyncSession, user_in: UserCreate):
        user_data = user_in.model_dump()
        user_data["hashed_password"] = hash_password(user_data.pop("password"))
        return await user_crud.create(session, user_data)

user_service = UserService()