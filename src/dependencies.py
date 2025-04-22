from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from src.database import async_session_maker
from src.exceptions import AccessDeniedException
from src.users.model import RoleEnum
from src.users.repository import UsersRepository, UserRolesRepository
from src.users.service import UsersService
from src.users.schemas import UserRead
from src.auth.service import AuthService
from src.services.repository import ServicesRepository
from src.services.service import ServicesService
from src.makes.repository import MakesRepository
from src.makes.service import MakesService


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_users_repository(async_session: AsyncSessionDep) -> UsersRepository:
    return UsersRepository(async_session)


def get_users_service(users_repository: Annotated[UsersRepository, Depends(get_users_repository)]) -> UsersService:
    return UsersService(users_repository)


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]


def get_user_roles_repository(async_session: AsyncSessionDep) -> UserRolesRepository:
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


def get_checker_user_roles(required_roles: list[RoleEnum]):
    def check_user_has_roles(current_user: CurrentUserByAccessTokenDep) -> UserRead:
        user_roles = [role for role in current_user.roles]

        if not any(required_role in user_roles for required_role in required_roles):
            raise AccessDeniedException()

        return current_user

    return check_user_has_roles


CurrentManagerDep = Annotated[UserRead, Depends(get_checker_user_roles([RoleEnum.manager]))]


def get_services_repository(async_session: AsyncSessionDep) -> ServicesRepository:
    return ServicesRepository(async_session)


def get_services_service(
        services_repository: Annotated[ServicesRepository, Depends(get_services_repository)]
) -> ServicesService:
    return ServicesService(services_repository)


ServicesServiceDep = Annotated[ServicesService, Depends(get_services_service)]


def get_makes_repository(async_session: AsyncSessionDep) -> MakesRepository:
    return MakesRepository(async_session)


def get_makes_service(makes_repository: Annotated[MakesRepository, Depends(get_makes_repository)]) -> MakesService:
    return MakesService(makes_repository)


MakesServiceDep = Annotated[MakesService, Depends(get_makes_service)]
