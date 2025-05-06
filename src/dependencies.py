from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from src.database import async_session_maker
from src.exceptions import AccessDeniedException
from src.users.model import RoleEnum
from src.users.repository import UsersRepository, UserRolesRepository
from src.users.service import UsersService, UserRolesService
from src.users.schemas import UserRead
from src.auth.service import AuthService
from src.vehicles.repository import VehiclesRepository
from src.vehicles.service import VehiclesService
from src.services.repository import ServicesRepository
from src.services.service import ServicesService
from src.makes.repository import MakesRepository
from src.makes.service import MakesService
from src.models.repository import ModelsRepository
from src.models.service import ModelsService
from src.ranges.repository import RangesRepository
from src.ranges.service import RangesService
from src.generations.repository import GenerationsRepository
from src.generations.service import GenerationsService
from src.configurations.repository import ConfigurationsRepository
from src.scrapers.service import DromScraperService


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


def get_user_roles_service(
        user_roles_repository: Annotated[UserRolesRepository, Depends(get_user_roles_repository)]
) -> UserRolesService:
    return UserRolesService(user_roles_repository)


UserRolesServiceDep = Annotated[UserRolesService, Depends(get_user_roles_service)]


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


CurrentOwnerDep = Annotated[UserRead, Depends(get_checker_user_roles([RoleEnum.owner]))]
CurrentManagerDep = Annotated[UserRead, Depends(get_checker_user_roles([RoleEnum.manager]))]
CurrentAdminDep = Annotated[UserRead, Depends(get_checker_user_roles([RoleEnum.admin]))]


def get_vehicles_repository(async_session: AsyncSessionDep) -> VehiclesRepository:
    return VehiclesRepository(async_session)


def get_vehicles_service(
        vehicles_repository: Annotated[VehiclesRepository, Depends(get_vehicles_repository)]
) -> VehiclesService:
    return VehiclesService(vehicles_repository)


VehiclesServiceDep = Annotated[VehiclesService, Depends(get_vehicles_service)]


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


def get_models_repository(async_session: AsyncSessionDep) -> ModelsRepository:
    return ModelsRepository(async_session)


def get_models_service(
        makes_repository: Annotated[MakesRepository, Depends(get_makes_repository)],
        models_repository: Annotated[ModelsRepository, Depends(get_models_repository)]
) -> ModelsService:
    return ModelsService(makes_repository, models_repository)


ModelsServiceDep = Annotated[ModelsService, Depends(get_models_service)]


def get_ranges_repository(async_session: AsyncSessionDep) -> RangesRepository:
    return RangesRepository(async_session)


def get_ranges_service(
        models_repository: Annotated[ModelsRepository, Depends(get_models_repository)],
        ranges_repository: Annotated[RangesRepository, Depends(get_ranges_repository)]
) -> RangesService:
    return RangesService(models_repository, ranges_repository)


RangesServiceDep = Annotated[RangesService, Depends(get_ranges_service)]


def get_generations_repository(async_session: AsyncSessionDep) -> GenerationsRepository:
    return GenerationsRepository(async_session)


def get_generations_service(
        ranges_repository: Annotated[RangesRepository, Depends(get_ranges_repository)],
        generations_repository: Annotated[GenerationsRepository, Depends(get_generations_repository)]
) -> GenerationsService:
    return GenerationsService(ranges_repository, generations_repository)


GenerationsServiceDep = Annotated[GenerationsService, Depends(get_generations_service)]


def get_configurations_repository(async_session: AsyncSessionDep) -> ConfigurationsRepository:
    return ConfigurationsRepository(async_session)


def get_drom_scraper_service(
        makes_repository: Annotated[MakesRepository, Depends(get_makes_repository)],
        models_repository: Annotated[ModelsRepository, Depends(get_models_repository)],
        ranges_repository: Annotated[RangesRepository, Depends(get_ranges_repository)],
        generations_repository: Annotated[GenerationsRepository, Depends(get_generations_repository)],
        configurations_repository: Annotated[ConfigurationsRepository, Depends(get_configurations_repository)]
) -> DromScraperService:
    return DromScraperService(
        makes_repository, models_repository, ranges_repository, generations_repository, configurations_repository
    )


DromScraperServiceDep = Annotated[DromScraperService, Depends(get_drom_scraper_service)]
