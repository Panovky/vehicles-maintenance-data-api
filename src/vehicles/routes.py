from fastapi import APIRouter, status
from src.dependencies import CurrentOwnerDep, VehiclesServiceDep
from .schemas import VehicleRead, VehicleCreate

router = APIRouter(
    prefix='/vehicles',
    tags=['vehicles']
)


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
        current_owner: CurrentOwnerDep, data: VehicleCreate, vehicles_service: VehiclesServiceDep
) -> VehicleRead:
    vehicle = await vehicles_service.create(data, current_owner.id)
    return vehicle
