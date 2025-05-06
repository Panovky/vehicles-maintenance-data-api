from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from .model import EngineTypeEnum, TransmissionEnum, DriveEnum


class ConfigurationRead(BaseModel):
    """The model representing the vehicle configuration data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    engine_capacity: Annotated[float | None, Field(example='1.3')]
    engine_power: Annotated[int | None, Field(example='149')]
    engine_type: EngineTypeEnum | None
    transmission: TransmissionEnum | None
    drive: DriveEnum | None
