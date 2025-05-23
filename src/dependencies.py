from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from src.core.jwt_service import JWTService
from src.core.email_service import EmailService
from src.database import async_session_maker
from src.exceptions import AccessDeniedException
from src.users.repository import UsersRepository
from src.users.service import UsersService
from src.users.schemas import UserRead
from src.user_roles.model import UserRoleEnum
from src.user_roles.repository import UserRolesRepository
from src.user_roles.service import UserRolesService
from src.auth.service import AuthService
from src.makes.repository import MakesRepository
from src.makes.service import MakesService
from src.models.repository import ModelsRepository
from src.models.service import ModelsService
from src.ranges.repository import RangesRepository
from src.ranges.service import RangesService
from src.generations.repository import GenerationsRepository
from src.generations.service import GenerationsService
from src.configurations.repository import ConfigurationsRepository
from src.configurations.service import ConfigurationsService
from src.scrapers.service import DromScraperService, EgrulEgripScraperService
from src.vehicles.repository import VehiclesRepository
from src.vehicles.service import VehiclesService
from src.services.repository import ServicesRepository
from src.services.service import ServicesService
from src.service_workers.repository import ServiceWorkersRepository
from src.service_workers.service import ServiceWorkersService
from src.service_clients.repository import ServiceClientsRepository
from src.service_clients.service import ServiceClientsService
from src.maintenance_records.repository import MaintenanceRecordsRepository
from src.maintenance_record_workers.repository import MaintenanceRecordWorkersRepository
from src.maintenance_record_photos.repository import MaintenanceRecordPhotosRepository
from src.maintenance_record_documents.repository import MaintenanceRecordDocumentsRepository
from src.maintenance_records.service import MaintenanceRecordsService


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_jwt_service() -> JWTService:
    return JWTService()


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


def get_email_service() -> EmailService:
    return EmailService()


EmailServiceDep = Annotated[EmailService, Depends(get_email_service)]


def get_users_repository(async_session: AsyncSessionDep) -> UsersRepository:
    return UsersRepository(async_session)


UsersRepositoryDep = Annotated[UsersRepository, Depends(get_users_repository)]


def get_users_service(users_repository: UsersRepositoryDep) -> UsersService:
    return UsersService(users_repository)


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]


def get_user_roles_repository(async_session: AsyncSessionDep) -> UserRolesRepository:
    return UserRolesRepository(async_session)


UserRolesRepositoryDep = Annotated[UserRolesRepository, Depends(get_user_roles_repository)]


def get_user_roles_service(user_roles_repository: UserRolesRepositoryDep) -> UserRolesService:
    return UserRolesService(user_roles_repository)


UserRolesServiceDep = Annotated[UserRolesService, Depends(get_user_roles_service)]


def get_auth_service(
        users_repository: UsersRepositoryDep,
        user_roles_repository: UserRolesRepositoryDep,
        jwt_service: JWTServiceDep,
        email_service: EmailServiceDep
) -> AuthService:
    return AuthService(users_repository, user_roles_repository, jwt_service, email_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_auth_header() -> HTTPBearer:
    return HTTPBearer()


AuthHeaderDep = Annotated[str, Depends(get_auth_header())]


async def get_current_user_by_access_token(auth_header: AuthHeaderDep, auth_service: AuthServiceDep) -> UserRead:
    return await auth_service.get_current_user_by_token(token=auth_header.credentials, token_type='access')


CurrentUserByAccessTokenDep = Annotated[UserRead, Depends(get_current_user_by_access_token)]


async def get_current_user_by_refresh_token(auth_header: AuthHeaderDep, auth_service: AuthServiceDep) -> UserRead:
    return await auth_service.get_current_user_by_token(token=auth_header.credentials, token_type='refresh')


CurrentUserByRefreshTokenDep = Annotated[UserRead, Depends(get_current_user_by_refresh_token)]


def get_checker_user_roles(required_roles: list[UserRoleEnum]):
    def check_user_has_roles(current_user: CurrentUserByAccessTokenDep) -> UserRead:
        user_roles = [role for role in current_user.roles]

        if not any(required_role in user_roles for required_role in required_roles):
            raise AccessDeniedException()

        return current_user

    return check_user_has_roles


CurrentOwnerDep = Annotated[UserRead, Depends(get_checker_user_roles([UserRoleEnum.owner]))]
CurrentManagerDep = Annotated[UserRead, Depends(get_checker_user_roles([UserRoleEnum.manager]))]
CurrentAdminDep = Annotated[UserRead, Depends(get_checker_user_roles([UserRoleEnum.admin]))]
CurrentOwnerOrWorkerDep = Annotated[
    UserRead, Depends(get_checker_user_roles([UserRoleEnum.owner, UserRoleEnum.worker]))
]


def get_makes_repository(async_session: AsyncSessionDep) -> MakesRepository:
    return MakesRepository(async_session)


MakesRepositoryDep = Annotated[MakesRepository, Depends(get_makes_repository)]


def get_makes_service(makes_repository: MakesRepositoryDep) -> MakesService:
    return MakesService(makes_repository)


MakesServiceDep = Annotated[MakesService, Depends(get_makes_service)]


def get_models_repository(async_session: AsyncSessionDep) -> ModelsRepository:
    return ModelsRepository(async_session)


ModelsRepositoryDep = Annotated[ModelsRepository, Depends(get_models_repository)]


def get_models_service(makes_repository: MakesRepositoryDep, models_repository: ModelsRepositoryDep) -> ModelsService:
    return ModelsService(makes_repository, models_repository)


ModelsServiceDep = Annotated[ModelsService, Depends(get_models_service)]


def get_ranges_repository(async_session: AsyncSessionDep) -> RangesRepository:
    return RangesRepository(async_session)


RangesRepositoryDep = Annotated[RangesRepository, Depends(get_ranges_repository)]


def get_ranges_service(models_repository: ModelsRepositoryDep, ranges_repository: RangesRepositoryDep) -> RangesService:
    return RangesService(models_repository, ranges_repository)


RangesServiceDep = Annotated[RangesService, Depends(get_ranges_service)]


def get_generations_repository(async_session: AsyncSessionDep) -> GenerationsRepository:
    return GenerationsRepository(async_session)


GenerationsRepositoryDep = Annotated[GenerationsRepository, Depends(get_generations_repository)]


def get_generations_service(
        ranges_repository: RangesRepositoryDep,
        generations_repository: GenerationsRepositoryDep
) -> GenerationsService:
    return GenerationsService(ranges_repository, generations_repository)


GenerationsServiceDep = Annotated[GenerationsService, Depends(get_generations_service)]


def get_configurations_repository(async_session: AsyncSessionDep) -> ConfigurationsRepository:
    return ConfigurationsRepository(async_session)


ConfigurationsRepositoryDep = Annotated[ConfigurationsRepository, Depends(get_configurations_repository)]


def get_configurations_service(
        generations_repository: GenerationsRepositoryDep,
        configurations_repository: ConfigurationsRepositoryDep,
) -> ConfigurationsService:
    return ConfigurationsService(generations_repository, configurations_repository)


ConfigurationsServiceDep = Annotated[ConfigurationsService, Depends(get_configurations_service)]


def get_drom_scraper_service(
        makes_repository: MakesRepositoryDep,
        models_repository: ModelsRepositoryDep,
        ranges_repository: RangesRepositoryDep,
        generations_repository: GenerationsRepositoryDep,
        configurations_repository: ConfigurationsRepositoryDep
) -> DromScraperService:
    return DromScraperService(
        makes_repository, models_repository, ranges_repository, generations_repository, configurations_repository
    )


DromScraperServiceDep = Annotated[DromScraperService, Depends(get_drom_scraper_service)]


def get_egrul_egrip_scraper_service() -> EgrulEgripScraperService:
    return EgrulEgripScraperService()


EgrulEgripScraperServiceDep = Annotated[EgrulEgripScraperService, Depends(get_egrul_egrip_scraper_service)]


def get_vehicles_repository(async_session: AsyncSessionDep) -> VehiclesRepository:
    return VehiclesRepository(async_session)


VehiclesRepositoryDep = Annotated[VehiclesRepository, Depends(get_vehicles_repository)]


def get_vehicles_service(
        makes_repository: MakesRepositoryDep,
        models_repository: ModelsRepositoryDep,
        ranges_repository: RangesRepositoryDep,
        generations_repository: GenerationsRepositoryDep,
        configurations_repository: ConfigurationsRepositoryDep,
        vehicles_repository: VehiclesRepositoryDep,
        users_repository: UsersRepositoryDep,
        user_roles_repository: UserRolesRepositoryDep,
        jwt_service: JWTServiceDep,
        email_service: EmailServiceDep
) -> VehiclesService:
    return VehiclesService(
        makes_repository,
        models_repository,
        ranges_repository,
        generations_repository,
        configurations_repository,
        vehicles_repository,
        users_repository,
        user_roles_repository,
        jwt_service,
        email_service
    )


VehiclesServiceDep = Annotated[VehiclesService, Depends(get_vehicles_service)]


def get_services_repository(async_session: AsyncSessionDep) -> ServicesRepository:
    return ServicesRepository(async_session)


ServicesRepositoryDep = Annotated[ServicesRepository, Depends(get_services_repository)]


def get_services_service(services_repository: ServicesRepositoryDep) -> ServicesService:
    return ServicesService(services_repository)


ServicesServiceDep = Annotated[ServicesService, Depends(get_services_service)]


def get_service_workers_repository(async_session: AsyncSessionDep) -> ServiceWorkersRepository:
    return ServiceWorkersRepository(async_session)


ServiceWorkersRepositoryDep = Annotated[ServiceWorkersRepository, Depends(get_service_workers_repository)]


def get_service_workers_service(
        users_repository: UsersRepositoryDep,
        user_roles_repository: UserRolesRepositoryDep,
        services_repository: ServicesRepositoryDep,
        service_workers_repository: ServiceWorkersRepositoryDep,
        jwt_service: JWTServiceDep,
        email_service: EmailServiceDep
) -> ServiceWorkersService:
    return ServiceWorkersService(
        users_repository,
        user_roles_repository,
        services_repository,
        service_workers_repository,
        jwt_service,
        email_service
    )


ServiceWorkersServiceDep = Annotated[ServiceWorkersService, Depends(get_service_workers_service)]


def get_service_clients_repository(async_session: AsyncSessionDep) -> ServiceClientsRepository:
    return ServiceClientsRepository(async_session)


ServiceClientsRepositoryDep = Annotated[ServiceClientsRepository, Depends(get_service_clients_repository)]


def get_service_clients_service(
        users_repository: UsersRepositoryDep,
        user_roles_repository: UserRolesRepositoryDep,
        services_repository: ServicesRepositoryDep,
        service_clients_repository: ServiceClientsRepositoryDep,
        jwt_service: JWTServiceDep,
        email_service: EmailServiceDep
) -> ServiceClientsService:
    return ServiceClientsService(
        users_repository,
        user_roles_repository,
        services_repository,
        service_clients_repository,
        jwt_service,
        email_service
    )


ServiceClientsServiceDep = Annotated[ServiceClientsService, Depends(get_service_clients_service)]


def get_maintenance_records_repository(async_session: AsyncSessionDep) -> MaintenanceRecordsRepository:
    return MaintenanceRecordsRepository(async_session)


MaintenanceRecordsRepositoryDep = Annotated[MaintenanceRecordsRepository, Depends(get_maintenance_records_repository)]


def get_maintenance_record_workers_repository(async_session: AsyncSessionDep) -> MaintenanceRecordWorkersRepository:
    return MaintenanceRecordWorkersRepository(async_session)


MaintenanceRecordWorkersRepositoryDep = Annotated[
    MaintenanceRecordWorkersRepository, Depends(get_maintenance_record_workers_repository)
]


def get_maintenance_record_photos_repository(async_session: AsyncSessionDep) -> MaintenanceRecordPhotosRepository:
    return MaintenanceRecordPhotosRepository(async_session)


MaintenanceRecordPhotosRepositoryDep = Annotated[
    MaintenanceRecordPhotosRepository, Depends(get_maintenance_record_photos_repository)
]


def get_maintenance_record_documents_repository(async_session: AsyncSessionDep) -> MaintenanceRecordDocumentsRepository:
    return MaintenanceRecordDocumentsRepository(async_session)


MaintenanceRecordDocumentsRepositoryDep = Annotated[
    MaintenanceRecordDocumentsRepository, Depends(get_maintenance_record_documents_repository)
]


def get_maintenance_records_service(
        maintenance_records_repository: MaintenanceRecordsRepositoryDep,
        maintenance_record_photos_repository: MaintenanceRecordPhotosRepositoryDep,
        maintenance_record_documents_repository: MaintenanceRecordDocumentsRepositoryDep,
        maintenance_record_workers_repository: MaintenanceRecordWorkersRepositoryDep
) -> MaintenanceRecordsService:
    return MaintenanceRecordsService(
        maintenance_records_repository,
        maintenance_record_photos_repository,
        maintenance_record_documents_repository,
        maintenance_record_workers_repository
    )


MaintenanceRecordsServiceDep = Annotated[MaintenanceRecordsService, Depends(get_maintenance_records_service)]
