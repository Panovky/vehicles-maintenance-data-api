from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import User


class UsersRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, User)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email).options(joinedload(User.roles))
        user = await self.async_session.execute(stmt)
        return user.scalar()
