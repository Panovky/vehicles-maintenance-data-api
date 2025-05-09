from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.sqlalchemy_repository import SQLAlchemyRepository
from .model import Model, ModelTypeEnum


class ModelsRepository(SQLAlchemyRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Model)

    async def get_by_make_id_model_type_and_prefix_alphabetically(
            self, make_id: int, model_type: ModelTypeEnum, prefix: str
    ) -> list[Model]:
        stmt = select(Model).where(and_(
            Model.make_id == make_id, Model.type == model_type, Model.name.ilike(f"{prefix}%"))
        ).order_by(Model.name)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def get_by_make_id_and_model_type_alphabetically(
            self, make_id: int, model_type: ModelTypeEnum
    ) -> list[Model]:
        stmt = select(Model).where(and_(Model.make_id == make_id, Model.type == model_type)).order_by(Model.name)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def get_by_make_id_and_prefix_alphabetically(self, make_id: int, prefix: str) -> list[Model]:
        stmt = select(Model).where(and_(Model.make_id == make_id, Model.name.ilike(f"{prefix}%"))).order_by(Model.name)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())

    async def get_by_make_id_alphabetically(self, make_id: int) -> list[Model]:
        stmt = select(Model).where(Model.make_id == make_id).order_by(Model.name)
        res = await self.async_session.execute(stmt)
        return list(res.scalars())
