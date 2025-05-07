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
    user_id: Annotated[int, Field(example=1)]
    make: MakeRead
    model: ModelRead
    range: RangeRead
    generation: GenerationRead
    configuration: ConfigurationRead
    color: VehicleColorEnum
    manufacture_year: Annotated[int, Field(example=2005)]
    mileage: Annotated[int, Field(example=175000)]
    vin: Annotated[str, Field(example='JHMCM56557C404453')]
    registration_plate: Annotated[str, Field(example='Е734МТ76')]


class VehicleCreate(BaseModel):
    """The model representing the vehicle data needed to create record in the database."""
    make_id: Annotated[int, Field(gt=0, example=1)]
    model_id: Annotated[int, Field(gt=0, example=1)]
    range_id: Annotated[int, Field(gt=0, example=1)]
    generation_id: Annotated[int, Field(gt=0, example=1)]
    configuration_id: Annotated[int, Field(gt=0, example=1)]
    color: VehicleColorEnum
    manufacture_year: Annotated[int, Field(gte=1900, example=2005)]
    mileage: Annotated[int, Field(gte=0, example=175000)]
    vin: Annotated[str, Field(pattern='^[A-HJ-NPR-Z0-9]{17}$', example='JHMCM56557C404453')]
    registration_plate: Annotated[str, Field(
        pattern='^[АВЕКМНОРСТУХ]{1}[0-9]{3}[АВЕКМНОРСТУХ]{2}[0-9]{2,3}$', example='Е734МТ76'
    )]
