from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class MaintenanceRecordDocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    document_path: Annotated[str, Field(example='/static/maintenance_records/documents/1.pdf')]
