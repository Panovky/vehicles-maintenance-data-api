from sqlalchemy.ext.asyncio import AsyncSession
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import Generation


class GenerationsRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Generation)
