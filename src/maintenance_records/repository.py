from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from src.maintenance_record_service_workers.model import MaintenanceRecordServiceWorker
from src.service_workers.model import ServiceWorker
from .model import MaintenanceRecord


class MaintenanceRecordsRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, MaintenanceRecord)

    async def get_by_id(self, _id: int) -> MaintenanceRecord | None:
        stmt = select(MaintenanceRecord).options(
            joinedload(MaintenanceRecord.responsible).joinedload(ServiceWorker.user),
            joinedload(MaintenanceRecord.photos),
            joinedload(MaintenanceRecord.documents),
            joinedload(MaintenanceRecord.maintenance_record_service_workers)
            .joinedload(MaintenanceRecordServiceWorker.service_worker)
            .joinedload(ServiceWorker.user)
        )
        maintenance_record = await self.async_session.execute(stmt)
        return maintenance_record.scalar()
