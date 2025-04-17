from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.sqlalchemy_repository import SQLAlchemyRepository
from .model import User, UserRole


class UsersRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, User)


class UserRolesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, UserRole)

    async def assign_role(self, user_id: int, role_id: int) -> UserRole:
        user_role = self.model(user_id=user_id, role_id=role_id)
        self.async_session.add(user_role)
        await self.async_session.commit()
        await self.async_session.refresh(user_role)
        return user_role
