from fastapi import Depends
from fastapi.security import HTTPBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_maker
from src.users.schemas import UserRead
from src.users.repository import UsersRepository, UserRolesRepository
from src.auth.service import AuthService
from src.makes.repository import MakesRepository
from src.makes.service import MakesService


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_users_repository(async_session: Annotated[AsyncSession, Depends(get_async_session)]) -> UsersRepository:
    return UsersRepository(async_session)


def get_user_roles_repository(async_session: Annotated[AsyncSession, Depends(get_async_session)]) \
        -> UserRolesRepository:
    return UserRolesRepository(async_session)


def get_auth_service(
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
        user_roles_repository: Annotated[UserRolesRepository, Depends(get_user_roles_repository)]
) -> AuthService:
    return AuthService(users_repository, user_roles_repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_auth_header() -> HTTPBearer:
    return HTTPBearer()


async def get_current_user_by_access_token(
    auth_header: Annotated[str, Depends(get_auth_header())], auth_service: AuthServiceDep
) -> UserRead:
    return await auth_service.get_current_user_by_token(token=auth_header.credentials, token_type='access')


CurrentUserByAccessTokenDep = Annotated[UserRead, Depends(get_current_user_by_access_token)]


async def get_current_user_by_refresh_token(
    auth_header: Annotated[str, Depends(get_auth_header())], auth_service: AuthServiceDep
) -> UserRead:
    return await auth_service.get_current_user_by_token(token=auth_header.credentials, token_type='refresh')


CurrentUserByRefreshTokenDep = Annotated[UserRead, Depends(get_current_user_by_refresh_token)]


def get_makes_repository(async_session: Annotated[AsyncSession, Depends(get_async_session)]) -> MakesRepository:
    return MakesRepository(async_session)


def get_makes_service(makes_repository: Annotated[MakesRepository, Depends(get_makes_repository)]) -> MakesService:
    return MakesService(makes_repository)


MakesServiceDep = Annotated[MakesService, Depends(get_makes_service)]
