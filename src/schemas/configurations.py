from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated
from src.models import EngineTypeEnum, TransmissionEnum, DriveEnum


class ConfigurationRead(BaseModel):
    """The model representing the vehicle configuration data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    engine_capacity: Annotated[float | None, Field(example='1.3')]
    engine_power: Annotated[int | None, Field(example='149')]
    engine_type: EngineTypeEnum | None
    transmission: TransmissionEnum | None
    drive: DriveEnum | None
