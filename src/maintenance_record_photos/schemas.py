from pydantic import BaseModel, Field
from typing import Annotated


class MaintenanceRecordPhotoRead(BaseModel):
    maintenance_record_id: Annotated[int, Field(example=1)]
    photo_path: Annotated[str, Field(example='/static/maintenance_records/photos/1.jpg')]
