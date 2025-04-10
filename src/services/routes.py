from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select
from typing import Annotated, Any
from src.dependencies import AsyncSessionDep
from src.utils.exceptions import ServiceNotFoundException
from src.entities import Service
from src.schemas import ServiceRead, ServiceCreate, ServiceUpdate

router = APIRouter(
    prefix='/services',
    tags=['services']
)


@router.get(
    '/{service_id}',
    responses={200: {'description': 'Service successfully received'}, 404: {'description': 'Service not found'}},
    summary='Return the service'
)
async def get_service(service_id: Annotated[int, Path(gt=0)], async_session: AsyncSessionDep) -> ServiceRead:
    """Return the service with the specified id"""
    service = await async_session.get(Service, service_id)
    if not service:
        raise ServiceNotFoundException()
    return service


@router.patch(
    '/{service_id}',
    responses={200: {'description': 'Service successfully updated'}, 404: {'description': 'Service not found'}},
    summary='Update the service'
)
async def update_service(
        service_id: Annotated[int, Path(gt=0)], service_data: ServiceUpdate, async_session: AsyncSessionDep
) -> ServiceRead:
    """Update the service with the specified id with the given information (blank values are ignored)"""
    service = await async_session.get(Service, service_id)
    if not service:
        raise ServiceNotFoundException()
    for key, value in service_data.model_dump(exclude_none=True).items():
        setattr(service, key, value)
    await async_session.commit()
    await async_session.refresh(service)
    return service


@router.delete(
    '/{service_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Service successfully deleted'},
        404: {'description': 'Service not found'},
    },
    summary='Delete the service'
)
async def delete_service(service_id: Annotated[int, Path(gt=0)], async_session: AsyncSessionDep) -> Response:
    """Delete the service with the specified id."""
    service = await async_session.get(Service, service_id)
    if not service:
        raise ServiceNotFoundException()
    await async_session.delete(service)
    await async_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/',
    responses={200: {'description': 'Services successfully received'}},
    summary='Return a list of services'
)
async def get_services(async_session: AsyncSessionDep, limit: int = 10, offset: int = 0) -> list[ServiceRead]:
    """Return a list of services of a given length (limit), starting from a given table entry (offset)."""
    result = await async_session.execute(select(Service).offset(offset).limit(limit))
    return result.scalars()


@router.post(
    '/',
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
    responses={201: {'description': 'Service successfully created'}},
    summary='Create the service'
)
async def create_service(service_data: ServiceCreate, async_session: AsyncSessionDep) -> Any:
    """Create the service with the given information."""
    service = Service(**service_data.model_dump())
    async_session.add(service)
    await async_session.commit()
    await async_session.refresh(service)
    return service
