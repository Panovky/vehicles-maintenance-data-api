from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import Make


class MakesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Make)

    async def get_all_alphabetically(self) -> list[Make]:
        stmt = select(Make).order_by(Make.name)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def get_by_prefix_alphabetically(self, prefix: str) -> list[Make]:
        stmt = select(Make).where(Make.name.ilike(f"{prefix}%")).order_by(Make.name)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())
