from pydantic import BaseModel, Field
from typing import Annotated
from src.service_workers.schemas import ServiceWorkerRead


class MaintenanceRecordServiceWorkerRead(BaseModel):
    maintenance_record_id: Annotated[int, Field(example=1)]
    service_worker: ServiceWorkerRead
