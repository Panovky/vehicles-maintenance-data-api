from fastapi import APIRouter, Path, status
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Any, Annotated
from src.dependencies import AsyncSessionDep
from src.exceptions import VehicleNotFoundException, VINIsNotUniqueException, RegistrationNumberIsNotUniqueException
from .model import Vehicle
from .schemas import VehicleRead, VehicleCreate, VehicleUpdate

router = APIRouter(
    prefix='/vehicles',
    tags=['vehicles']
)


@router.get(
    '/{vehicle_id}',
    responses={200: {'description': 'Vehicle successfully received'}, 404: {'description': 'Vehicle not found'}},
    summary='Return the vehicle'
)
async def get_vehicle(vehicle_id: Annotated[int, Path(gt=0)], async_session: AsyncSessionDep) -> VehicleRead:
    """Return the vehicle with the specified id."""
    vehicle = await async_session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise VehicleNotFoundException()
    return vehicle


@router.patch(
    '/{vehicle_id}',
    responses={
        200: {'description': 'Vehicle successfully updated'},
        404: {'description': 'Vehicle not found'},
        409: {'description': 'Vehicle data is not unique'}
    },
    summary='Update the vehicle'
)
async def update_vehicle(
        vehicle_id: Annotated[int, Path(gt=0)], vehicle_data: VehicleUpdate, async_session: AsyncSessionDep
) -> VehicleRead:
    """Update the vehicle with the specified id with the given information (blank values are ignored)."""
    vehicle = await async_session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise VehicleNotFoundException()

    if vehicle_data.vin:
        stmt = select(exists().where(and_(Vehicle.vin == vehicle_data.vin, Vehicle.id != vehicle_id)))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise VINIsNotUniqueException()

    if vehicle_data.registration_number:
        stmt = select(exists().where(and_(
            Vehicle.registration_number == vehicle_data.registration_number, Vehicle.id != vehicle_id
        )))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise RegistrationNumberIsNotUniqueException()

    for key, value in vehicle_data.model_dump(exclude_none=True).items():
        if key != 'color':
            setattr(vehicle, key, value)
        else:
            setattr(vehicle, key, value.value)
    await async_session.commit()
    await async_session.refresh(vehicle)
    return vehicle


@router.delete(
    '/{vehicle_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Vehicle successfully deleted'}, 404: {'description': 'Vehicle not found'}
    },
    summary='Delete the vehicle'
)
async def delete_vehicle(vehicle_id: Annotated[int, Path(gt=0)], async_session: AsyncSessionDep) -> Response:
    """Delete the vehicle with the specified id."""
    vehicle = await async_session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise VehicleNotFoundException()
    await async_session.delete(vehicle)
    await async_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/',
    responses={200: {'description': 'Vehicles successfully received'}},
    summary='Return a list of vehicles'
)
async def get_vehicles(async_session: AsyncSessionDep, limit: int = 10, offset: int = 0) -> list[VehicleRead]:
    """Return a list of vehicles of a given length (limit), starting from a given table entry (offset)."""
    result = await async_session.execute(select(Vehicle).offset(offset).limit(limit))
    return result.scalars()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VehicleRead,
    responses={
        201: {'description': 'Vehicle successfully created'}, 409: {'description': 'Vehicle data is not unique'}
    },
    summary='Create the vehicle'
)
async def create_vehicle(vehicle_data: VehicleCreate, async_session: AsyncSessionDep) -> Any:
    """Create the vehicle with the given information."""

    stmt = select(exists().where(Vehicle.vin == vehicle_data.vin))
    result = await async_session.execute(stmt)
    if result.scalar():
        raise VINIsNotUniqueException()

    stmt = select(exists().where(Vehicle.registration_number == vehicle_data.registration_number))
    result = await async_session.execute(stmt)
    if result.scalar():
        raise RegistrationNumberIsNotUniqueException()

    vehicle_data_dict = {key: value for key, value in vehicle_data.model_dump().items() if key != 'color'}
    vehicle = Vehicle(**vehicle_data_dict, color=vehicle_data.color.value)
    async_session.add(vehicle)
    await async_session.commit()
    await async_session.refresh(vehicle)
    return vehicle
