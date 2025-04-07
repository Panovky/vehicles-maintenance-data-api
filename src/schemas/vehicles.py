from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated
from src.models import VehicleColorEnum


class VehicleRead(BaseModel):
    """The model representing the vehicle data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    user_id: Annotated[int, Field(example=1)]
    make_id: Annotated[int, Field(example=1)]
    model_id: Annotated[int, Field(example=1)]
    range_id: Annotated[int, Field(example=1)]
    generation_id: Annotated[int, Field(example=1)]
    configuration_id: Annotated[int, Field(example=1)]
    color: VehicleColorEnum
    manufacture_year: Annotated[int, Field(example=2005)]
    mileage: Annotated[int, Field(example=175000)]
    vin: Annotated[str, Field(example='JHMCM56557C404453')]
    registration_number: Annotated[str, Field(example='Е734МТ76')]


class VehicleCreate(BaseModel):
    """The model representing the vehicle data needed to create record in the database."""
    user_id: Annotated[int, Field(gt=0, example=1)]
    make_id: Annotated[int, Field(gt=0, example=1)]
    model_id: Annotated[int, Field(gt=0, example=1)]
    range_id: Annotated[int, Field(gt=0, example=1)]
    generation_id: Annotated[int, Field(gt=0, example=1)]
    configuration_id: Annotated[int, Field(gt=0, example=1)]
    color: VehicleColorEnum
    manufacture_year: Annotated[int, Field(gte=1950, example=2005)]
    mileage: Annotated[int, Field(gte=0, example=175000)]
    vin: Annotated[str, Field(pattern='^[A-HJ-NPR-Z0-9]{17}$', example='JHMCM56557C404453')]
    registration_number: Annotated[str, Field(
        pattern='^[АВЕКМНОРСТУХ]{1}[0-9]{3}[АВЕКМНОРСТУХ]{2}[0-9]{2,3}$', example='Е734МТ76'
    )]


class VehicleUpdate(BaseModel):
    """The model representing the vehicle data needed to update information in the database."""
    user_id: Annotated[int | None, Field(gt=0, default=None, example=1)]
    make_id: Annotated[int | None, Field(gt=0, default=None, example=1)]
    model_id: Annotated[int | None, Field(gt=0, default=None, example=1)]
    range_id: Annotated[int | None, Field(gt=0, default=None, example=1)]
    generation_id: Annotated[int | None, Field(gt=0, default=None, example=1)]
    configuration_id: Annotated[int | None, Field(gt=0, default=None, example=1)]
    color: Annotated[VehicleColorEnum | None, Field(default=None)]
    manufacture_year: Annotated[int | None, Field(gte=1950, default=None, example=2005)]
    mileage: Annotated[int | None, Field(gte=0, default=None, example=175000)]
    vin: Annotated[str | None, Field(pattern='^[A-HJ-NPR-Z0-9]{17}$', default=None, example='JHMCM56557C404453')]
    registration_number: Annotated[str | None, Field(
        pattern='^[АВЕКМНОРСТУХ]{1}[0-9]{3}[АВЕКМНОРСТУХ]{2}[0-9]{2,3}$', default=None, example='Е734МТ76'
    )]
