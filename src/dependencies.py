from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_maker
from src.makes.repository import MakesRepository
from src.makes.service import MakesService


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_makes_repository(async_session: Annotated[AsyncSession, Depends(get_async_session)]) -> MakesRepository:
    return MakesRepository(async_session)


def get_makes_service(makes_repository: Annotated[MakesRepository, Depends(get_makes_repository)]) -> MakesService:
    return MakesService(makes_repository)


MakesServiceDep = Annotated[MakesService, Depends(get_makes_service)]
