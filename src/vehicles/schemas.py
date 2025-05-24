from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from src.makes.schemas import MakeRead
from src.models.schemas import ModelRead
from src.ranges.schemas import RangeRead
from src.generations.schemas import GenerationRead
from src.configurations.schemas import ConfigurationRead
from .model import VehicleColorEnum


class VehicleRead(BaseModel):
    """The model representing the vehicle data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    owner_id: Annotated[int, Field(example=1)]
    photo_path: Annotated[str, Field(example='/static/vehicles/photos/123e4567e89b12d3a456426614174000.jpg')]
    make: MakeRead
    model: ModelRead
    range: RangeRead
    generation: GenerationRead
    configuration: ConfigurationRead
    color: VehicleColorEnum
    manufacture_year: Annotated[int, Field(example=2005)]
    mileage: Annotated[int, Field(example=175000)]
    vin: Annotated[str, Field(example='JHMCM56557C404453')]
    registration_plate: Annotated[str, Field(example='E734MT76')]
