from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import Vehicle


class VehiclesRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Vehicle)

    async def get_by_id(self, _id: int) -> Vehicle | None:
        stmt = select(Vehicle).where(Vehicle.id == _id).options(
            joinedload(Vehicle.make),
            joinedload(Vehicle.model),
            joinedload(Vehicle.range),
            joinedload(Vehicle.generation),
            joinedload(Vehicle.configuration),
        )
        vehicle = await self.async_session.execute(stmt)
        return vehicle.scalar()

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

    async def update(self, _id: int, data: dict) -> Vehicle | None:
        vehicle = await self.get_by_id(_id)
        if not vehicle:
            return None

        for key, value in data.items():
            setattr(vehicle, key, value)

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

    async def filter_by(self, **filters) -> list[Vehicle]:
        stmt = select(Vehicle).options(
            joinedload(Vehicle.make),
            joinedload(Vehicle.model),
            joinedload(Vehicle.range),
            joinedload(Vehicle.generation),
            joinedload(Vehicle.configuration),
        ).filter_by(**filters)
        vehicles = await self.async_session.execute(stmt)
        return list(vehicles.scalars())
