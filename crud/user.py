from models.user import User
from schemas.user import UserSaveDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDUser:
    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, user_in: UserSaveDB) -> User:
        user = User(**user_in)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


user_crud = CRUDUser()