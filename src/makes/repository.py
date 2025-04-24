from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.sqlalchemy_repository import SQLAlchemyRepository
from .model import Make


class MakesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Make)

    async def get_by_name(self, name: str) -> Make | None:
        stmt = select(Make).where(Make.name == name)
        make = await self.async_session.execute(stmt)
        return make.scalar()
