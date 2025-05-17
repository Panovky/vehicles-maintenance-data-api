from sqlalchemy.ext.asyncio import AsyncSession
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import ServiceClient


class ServiceClientsRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, ServiceClient)
