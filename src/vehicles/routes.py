from fastapi import APIRouter, status, Form, UploadFile, File
from typing import Annotated
from src.dependencies import CurrentOwnerDep, VehiclesServiceDep
from .schemas import VehicleColorEnum, VehicleRead

router = APIRouter(
    prefix='/vehicles',
    tags=['vehicles']
)


@router.get(
    '/me',
    responses={
        200: {'description': 'Vehicles successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Get current owner vehicles'
)
async def get_owner_vehicles(
        current_owner: CurrentOwnerDep, vehicles_service: VehiclesServiceDep
) -> list[VehicleRead]:
    return await vehicles_service.get_owner_vehicles(current_owner.id)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Vehicle successfully created'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Make, model, range, generation or configuration not found'},
        409: {'description': 'VIN or registration plate is not unique'}
    },
    summary='Create the vehicle by current owner'
)
async def create_vehicle(
        current_owner: CurrentOwnerDep,
        make_id: Annotated[int, Form(gt=0)],
        model_id: Annotated[int, Form(gt=0)],
        range_id: Annotated[int, Form(gt=0)],
        generation_id: Annotated[int, Form(gt=0)],
        configuration_id: Annotated[int, Form(gt=0)],
        color: Annotated[VehicleColorEnum, Form()],
        manufacture_year: Annotated[int, Form(ge=1900)],
        mileage: Annotated[int, Form(ge=0)],
        vin: Annotated[str, Form(pattern='^[A-HJ-NPR-Z0-9]{17}$')],
        registration_plate: Annotated[str, Form(pattern='^[ABEKMHOPCTYX]{1}[0-9]{3}[ABEKMHOPCTYX]{2}[0-9]{2,3}$')],
        vehicles_service: VehiclesServiceDep,
        photo: Annotated[UploadFile | None, File()] = None
) -> VehicleRead:
    vehicle = await vehicles_service.create(
        {
            'make_id': make_id,
            'model_id': model_id,
            'range_id': range_id,
            'generation_id': generation_id,
            'configuration_id': configuration_id,
            'color': color,
            'manufacture_year': manufacture_year,
            'mileage': mileage,
            'vin': vin,
            'registration_plate': registration_plate
        },
        photo,
        current_owner.id
    )
    return vehicle
