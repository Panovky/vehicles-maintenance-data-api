from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.sqlalchemy_repository import SQLAlchemyRepository
from .model import UserRole, UserRoleEnum


class UserRolesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, UserRole)

    async def assign_role(self, user_id: int, role: UserRoleEnum) -> UserRole:
        user_role = self.model(user_id=user_id, role=role)
        self.async_session.add(user_role)
        await self.async_session.commit()
        await self.async_session.refresh(user_role)
        return user_role
