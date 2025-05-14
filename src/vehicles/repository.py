from sqlalchemy.ext.asyncio import AsyncSession
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import Vehicle


class VehiclesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Vehicle)

    async def create(self, data: dict) -> Vehicle:
        vehicle = self.model(**data)
        self.async_session.add(vehicle)
        await self.async_session.commit()
        await self.async_session.refresh(
            vehicle,
            [
                'make',
                'model',
                'range',
                'generation',
                'configuration'
            ]
        )
        return vehicle
