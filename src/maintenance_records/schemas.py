import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from .model import MaintenancePerformerEnum
from src.maintenance_record_photos.schemas import MaintenanceRecordPhotoRead
from src.maintenance_record_documents.schemas import MaintenanceRecordDocumentRead
from src.service_workers.schemas import ServiceWorkerRead


class MaintenanceRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    title: Annotated[str, Field(example='Замена масла и масляного фильтра')]
    maintenance_performer: Annotated[
        MaintenancePerformerEnum, Field(example=MaintenancePerformerEnum.registered_service)
    ]
    date: datetime.date
    vehicle_id: Annotated[int, Field(example=1)]
    mileage: Annotated[int, Field(example=180000)]
    service_id: Annotated[int | None, Field(example=1)]
    responsible: ServiceWorkerRead | None
    description: str | None
    parts_cost: Annotated[int, Field(example=5300)]
    labor_cost: Annotated[int, Field(example=2500)]
    total_cost: Annotated[int, Field(example=7800)]
    photos: list[MaintenanceRecordPhotoRead] | None
    documents: list[MaintenanceRecordDocumentRead] | None
    service_workers: list[ServiceWorkerRead] | None
