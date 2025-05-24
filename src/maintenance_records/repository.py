from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import MaintenanceRecord


class MaintenanceRecordsRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, MaintenanceRecord)

    async def get_by_id(self, _id: int) -> MaintenanceRecord | None:
        stmt = select(MaintenanceRecord).options(
            joinedload(MaintenanceRecord.responsible),
            joinedload(MaintenanceRecord.photos),
            joinedload(MaintenanceRecord.documents),
            joinedload(MaintenanceRecord.maintenance_record_workers)
        )
        maintenance_record = await self.async_session.execute(stmt)
        return maintenance_record.scalar()
