from fastapi import APIRouter, status
from src.dependencies import CurrentManagerDep, ServicesServiceDep
from .schemas import ServiceRead, ServiceCreate

router = APIRouter(
    prefix='/services',
    tags=['services']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Service successfully created'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Create the service'
)
async def create_service(
        current_manager: CurrentManagerDep, data: ServiceCreate, services_service: ServicesServiceDep
) -> ServiceRead:
    service = await services_service.create(data, current_manager.id)
    return service
