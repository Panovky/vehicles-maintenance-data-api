import datetime
from fastapi import APIRouter, status, UploadFile, File, Form
from typing import Annotated
from src.dependencies import CurrentOwnerOrWorkerDep, MaintenanceRecordsServiceDep
from .model import MaintenancePerformerEnum
from .schemas import MaintenanceRecordRead

router = APIRouter(
    tags=['maintenance records']
)


@router.post(
    '/maintenance-records',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Maintenance record successfully created'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Create the maintenance record by current owner or worker'
)
async def create_maintenance_record(
        current_owner_or_worker: CurrentOwnerOrWorkerDep,
        title: Annotated[str, Form(max_length=100)],
        maintenance_performer: Annotated[MaintenancePerformerEnum, Form()],
        date: Annotated[datetime.date, Form()],
        vehicle_id: Annotated[int, Form(gt=0)],
        mileage: Annotated[int, Form(gt=0)],
        maintenance_records_service: MaintenanceRecordsServiceDep,
        service_id: Annotated[int | None, Form(gt=0)] = None,
        responsible_id: Annotated[int | None, Form(gt=0)] = None,
        description: Annotated[str | None, Form(max_length=2000)] = None,
        parts_cost: Annotated[int, Form(gte=0)] = 0,
        labor_cost: Annotated[int, Form(gte=0)] = 0,
        total_cost: Annotated[int, Form(gte=0)] = 0,
        photos: Annotated[list[UploadFile] | None, File()] = None,
        documents: Annotated[list[UploadFile] | None, File()] = None,
        workers_ids: Annotated[str, Form()] = None
) -> MaintenanceRecordRead:
    return await maintenance_records_service.create(
        {
            'title': title,
            'maintenance_performer': maintenance_performer,
            'service_id': service_id,
            'responsible_id': responsible_id,
            'date': date,
            'vehicle_id': vehicle_id,
            'mileage': mileage,
            'description': description,
            'parts_cost': parts_cost,
            'labor_cost': labor_cost,
            'total_cost': total_cost
        },
        photos,
        documents,
        workers_ids
    )
