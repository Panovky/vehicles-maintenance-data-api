from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_maker
from src.users.repository import UsersRepository
from src.auth.service import AuthService
from src.makes.repository import MakesRepository
from src.makes.service import MakesService


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_users_repository(async_session: Annotated[AsyncSession, Depends(get_async_session)]) -> UsersRepository:
    return UsersRepository(async_session)


def get_auth_service(users_repository: Annotated[UsersRepository, Depends(get_users_repository)]) -> AuthService:
    return AuthService(users_repository)


def get_makes_repository(async_session: Annotated[AsyncSession, Depends(get_async_session)]) -> MakesRepository:
    return MakesRepository(async_session)


def get_makes_service(makes_repository: Annotated[MakesRepository, Depends(get_makes_repository)]) -> MakesService:
    return MakesService(makes_repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
MakesServiceDep = Annotated[MakesService, Depends(get_makes_service)]
