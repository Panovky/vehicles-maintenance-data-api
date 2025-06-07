from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class MaintenanceRecordPhotoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    photo_path: Annotated[str, Field(example='/static/maintenance_records/photos/1.jpg')]
