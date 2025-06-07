from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import MaintenanceRecord


class MaintenanceRecordsRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, MaintenanceRecord)

    async def get_by_id(self, _id: int) -> MaintenanceRecord | None:
        stmt = select(MaintenanceRecord).where(MaintenanceRecord.id == _id).options(
            joinedload(MaintenanceRecord.responsible),
            selectinload(MaintenanceRecord.photos),
            selectinload(MaintenanceRecord.documents),
            selectinload(MaintenanceRecord.maintenance_record_workers)
        )
        maintenance_record = await self.async_session.execute(stmt)
        return maintenance_record.scalar()

    async def filter_by(self, **filters) -> list[MaintenanceRecord]:
        stmt = select(MaintenanceRecord).filter_by(**filters).options(
            joinedload(MaintenanceRecord.responsible),
            selectinload(MaintenanceRecord.photos),
            selectinload(MaintenanceRecord.documents),
            selectinload(MaintenanceRecord.maintenance_record_workers)
        )
        maintenance_records = await self.async_session.execute(stmt)
        return list(maintenance_records.scalars())
