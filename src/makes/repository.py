from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import SQLAlchemyRepository
from .model import Make


class MakesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Make)
