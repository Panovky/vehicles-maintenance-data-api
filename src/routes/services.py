from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import ServiceNotFoundException
from src.models import Service
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
def get_service(service_id: Annotated[int, Path(gt=0)], session: SessionDep) -> ServiceRead:
    """Return the service with the specified id"""
    service = session.get(Service, service_id)
    if not service:
        raise ServiceNotFoundException()
    return service


@router.patch(
    '/{service_id}',
    responses={200: {'description': 'Service successfully updated'}, 404: {'description': 'Service not found'}},
    summary='Update the service'
)
def update_service(
        service_id: Annotated[int, Path(gt=0)], service_data: ServiceUpdate, session: SessionDep
) -> ServiceRead:
    """Update the service with the specified id with the given information (blank values are ignored)"""
    service = session.get(Service, service_id)
    if not service:
        raise ServiceNotFoundException()
    for key, value in service_data.model_dump(exclude_none=True).items():
        setattr(service, key, value)
    session.commit()
    session.refresh(service)
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
def delete_service(service_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the service with the specified id."""
    service = session.get(Service, service_id)
    if not service:
        raise ServiceNotFoundException()
    session.delete(service)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/',
    responses={200: {'description': 'Services successfully received'}},
    summary='Return a list of services'
)
def get_services(session: SessionDep, limit: int = 10, offset: int = 0) -> list[ServiceRead]:
    """Return a list of services of a given length (limit), starting from a given table entry (offset)."""
    services = session.execute(select(Service).offset(offset).limit(limit)).scalars()
    return services


@router.post(
    '/',
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
    responses={201: {'description': 'Service successfully created'}},
    summary='Create the service'
)
def create_service(service_data: ServiceCreate, session: SessionDep) -> Any:
    """Create the service with the given information."""
    service = Service(**service_data.model_dump())
    session.add(service)
    session.commit()
    session.refresh(service)
    return service
