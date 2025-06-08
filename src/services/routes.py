from fastapi import APIRouter, Path, status, Query
from src.dependencies import CurrentManagerDep, CurrentUserByAccessTokenDep, ServicesServiceDep
from .schemas import ServiceCreate, ServiceRead, ServiceUpdate
from typing import Annotated

router = APIRouter(
    prefix='/services',
    tags=['services']
)


@router.get(
    '/me',
    responses={
        200: {'description': 'Services successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Get current manager services'
)
async def get_manager_services(
        current_manager: CurrentManagerDep, services_service: ServicesServiceDep
) -> list[ServiceRead]:
    return await services_service.get_manager_services(current_manager.id)


@router.get(
    '/{service_id}',
    responses={
        200: {'description': 'Service successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'User email is not verified'},
        404: {'description': 'Service not found'}
    },
    summary='Get the service by id'
)
async def get_service(
        current_user: CurrentUserByAccessTokenDep,
        service_id: Annotated[int, Path(gt=0)],
        services_service: ServicesServiceDep
) -> ServiceRead:
    return await services_service.get_by_id(service_id)


@router.patch(
    '/{service_id}',
    responses={
        200: {'description': 'Service successfully updated'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Service not found'}
    },
    summary='Update the service'
)
async def update_service(
        current_manager: CurrentManagerDep,
        service_id: Annotated[int, Path(gt=0)],
        data: ServiceUpdate,
        services_service: ServicesServiceDep
) -> ServiceRead:
    service = await services_service.update(service_id, data)
    return service


@router.get(
    '',
    responses={
        200: {'description': 'Services successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'User email is not verified'}
    },
    summary='Get all services'
)
async def get_services(
        current_user: CurrentUserByAccessTokenDep,
        services_service: ServicesServiceDep,
        worker_id: Annotated[int | None, Query(gt=0, description='To get worker services')] = None,
        client_id: Annotated[int | None, Query(gt=0, description='To get client services')] = None
) -> list[ServiceRead]:
    return await services_service.get_all(worker_id, client_id)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Service successfully created'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        409: {'description': 'INN or OGRN is not unique'}
    },
    summary='Create the service by current manager'
)
async def create_service(
        current_manager: CurrentManagerDep, data: ServiceCreate, services_service: ServicesServiceDep
) -> ServiceRead:
    return await services_service.create(data, current_manager.id)
