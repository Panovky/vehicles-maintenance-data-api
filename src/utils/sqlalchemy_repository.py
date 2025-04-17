from typing import TypeVar, Generic
from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_
from .abstract_repository import AbstractRepository

T = TypeVar('T')


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    def __init__(self, async_session: AsyncSession, model: T):
        self.async_session: AsyncSession = async_session
        self.model: T = model

    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def get_by_id(self, _id: int) -> T | None:
        res = await self.async_session.get(self.model, _id)
        return res

    async def create(self, data: dict) -> T:
        instance = self.model(**data)
        self.async_session.add(instance)
        await self.async_session.commit()
        await self.async_session.refresh(instance)
        return instance

    async def update(self, _id: int, data: dict) -> T | None:
        instance = await self.get_by_id(_id)
        if not instance:
            return None

        for key, value in data.items():
            setattr(instance, key, value)

        await self.async_session.commit()
        await self.async_session.refresh(instance)
        return instance

    async def delete(self, _id: int) -> bool:
        instance = await self.get_by_id(_id)
        if not instance:
            return False

        await self.async_session.delete(instance)
        await self.async_session.commit()
        return True

    async def filter_by(self, **filters) -> list[T]:
        stmt = select(self.model).filter_by(**filters)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def starts_with(self, atr_name: str, prefix: str, case_sensitive: bool = False) -> list[T]:
        atr = getattr(self.model, atr_name)
        stmt = select(self.model)

        if case_sensitive:
            stmt = stmt.where(atr.startswith(prefix))
        else:
            stmt = stmt.where(func.lower(atr).startswith(prefix.lower()))

        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def exists(self, **filters) -> bool:
        conditions = [getattr(self.model, key) == value for key, value in filters.items()]
        stmt = select(exists().where(and_(*conditions)))
        res = await self.async_session.execute(stmt)
        return res.scalar()
