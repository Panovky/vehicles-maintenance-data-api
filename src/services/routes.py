from fastapi import APIRouter, Path
from src.dependencies import CurrentUserByAccessTokenDep, ServicesServiceDep
from .schemas import ServiceRead
from typing import Annotated

router = APIRouter(
    prefix='/services',
    tags=['services']
)


@router.get(
    '/{service_id}',
    responses={
        200: {'description': 'Service successfully received'},
        401: {'description': 'Access token are invalid'},
        404: {'description': 'Service not found'}
    },
    summary='Get the service by id'
)
async def get_service(
        current_user: CurrentUserByAccessTokenDep,
        service_id: Annotated[int, Path(gt=0)],
        services_service: ServicesServiceDep
) -> ServiceRead:
    service = await services_service.get_by_id(service_id)
    return service


@router.get(
    '',
    responses={
        200: {'description': 'Services successfully received'},
        401: {'description': 'Access token are invalid'}
    },
    summary='Get all services'
)
async def get_services(
        current_user: CurrentUserByAccessTokenDep,
        services_service: ServicesServiceDep
) -> list[ServiceRead]:
    services = await services_service.get_all()
    return services
