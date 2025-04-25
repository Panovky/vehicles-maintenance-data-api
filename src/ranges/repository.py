from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.sqlalchemy_repository import SQLAlchemyRepository
from .model import Range


class RangesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Range)
