from pydantic import BaseModel, Field
from typing import Annotated


class MaintenanceRecordDocumentRead(BaseModel):
    maintenance_record_id: Annotated[int, Field(example=1)]
    document_path: Annotated[str, Field(example='/static/maintenance_records/documents/1.pdf')]
