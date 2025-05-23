from sqlalchemy.ext.asyncio import AsyncSession
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import MaintenanceRecordServiceWorker


class MaintenanceRecordWorkersRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, MaintenanceRecordServiceWorker)
