from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import ServiceWorker


class ServiceWorkersRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, ServiceWorker)

    async def filter_by(self, **filters) -> list[ServiceWorker]:
        stmt = select(ServiceWorker).options(joinedload(ServiceWorker.user)).filter_by(**filters)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())
