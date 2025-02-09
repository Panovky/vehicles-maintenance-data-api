from fastapi import APIRouter, Path, status
from fastapi.responses import Response
from sqlalchemy import select, exists
from typing import Any, Annotated
from src.dependencies import SessionDep
from src.exceptions import VehicleNotFoundException, VINIsNotUniqueException, RegistrationNumberIsNotUniqueException
from src.models import Vehicle
from src.schemas import VehicleRead, VehicleCreate, VehicleUpdate

router = APIRouter(
    prefix='/vehicles',
    tags=['vehicles']
)


@router.get(
    '/{vehicle_id}',
    responses={200: {'description': 'Vehicle successfully received'}, 404: {'description': 'Vehicle not found'}},
    summary='Return the vehicle'
)
def get_vehicle(vehicle_id: Annotated[int, Path(gt=0)], session: SessionDep) -> VehicleRead:
    """Return the vehicle with the specified id."""
    vehicle = session.get(Vehicle, vehicle_id)
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
def update_vehicle(
        vehicle_id: Annotated[int, Path(gt=0)], vehicle_data: VehicleUpdate, session: SessionDep
) -> VehicleRead:
    """Update the vehicle with the specified id with the given information (blank values are ignored)."""
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise VehicleNotFoundException()

    if vehicle_data.vin:
        stmt = select(exists().where(Vehicle.vin == vehicle_data.vin))
        if session.execute(stmt).scalar():
            raise VINIsNotUniqueException()

    if vehicle_data.registration_number:
        stmt = select(exists().where(Vehicle.registration_number == vehicle_data.registration_number))
        if session.execute(stmt).scalar():
            raise RegistrationNumberIsNotUniqueException()

    for key, value in vehicle_data.model_dump(exclude_none=True).items():
        if key != 'color':
            setattr(vehicle, key, value)
        else:
            setattr(vehicle, key, value.value)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.delete(
    '/{vehicle_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Vehicle successfully deleted'}, 404: {'description': 'Vehicle not found'}
    },
    summary='Delete the vehicle'
)
def delete_vehicle(vehicle_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the vehicle with the specified id."""
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise VehicleNotFoundException()
    session.delete(vehicle)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/',
    responses={200: {'description': 'Vehicles successfully received'}},
    summary='Return a list of vehicles'
)
def get_vehicles(session: SessionDep, limit: int = 10, offset: int = 0) -> list[VehicleRead]:
    """Return a list of vehicles of a given length (limit), starting from a given table entry (offset)."""
    vehicles = session.execute(select(Vehicle).offset(offset).limit(limit)).scalars()
    return vehicles


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VehicleRead,
    responses={
        201: {'description': 'Vehicle successfully created'}, 409: {'description': 'Vehicle data is not unique'}
    },
    summary='Create the vehicle'
)
def create_vehicle(vehicle_data: VehicleCreate, session: SessionDep) -> Any:
    """Create the vehicle with the given information."""

    stmt = select(exists().where(Vehicle.vin == vehicle_data.vin))
    if session.execute(stmt).scalar():
        raise VINIsNotUniqueException()

    stmt = select(exists().where(Vehicle.registration_number == vehicle_data.registration_number))
    if session.execute(stmt).scalar():
        raise RegistrationNumberIsNotUniqueException()

    vehicle_data_dict = {key: value for key, value in vehicle_data.model_dump().items() if key != 'color'}
    vehicle = Vehicle(**vehicle_data_dict, color=vehicle_data.color.value)
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle

