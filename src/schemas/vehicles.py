from pydantic import BaseModel, Field
from typing import Annotated


class MakeRead(BaseModel):
    """The model representing the vehicle make data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    name: Annotated[str, Field(example='Renault')]


class ModelRead(BaseModel):
    """The model representing the vehicle model data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    name: Annotated[str, Field(example='Duster')]


class RangeRead(BaseModel):
    """The model representing the vehicles model range data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    name: Annotated[str, Field(example='Модельный ряд Renault Duster для России')]


class GenerationRead(BaseModel):
    """The model representing the vehicle generation data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    photo_url: Annotated[str, Field(example='https://www.drom.ru/catalog/renault/duster/g_2020_12623/')]
    full_name: Annotated[str, Field(example='Renault Duster (HM)\n11.2020 - 07.2022')]
    short_name: Annotated[str, Field(example='2 поколение')]
    vehicle_body: Annotated[str, Field(example='Джип/SUV 5 дв.')]


class ConfigurationRead(BaseModel):
    """The model representing the vehicle configuration data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    engine_capacity: Annotated[float, Field(example='1.3')]
    engine_power: Annotated[int, Field(example='149')]
    engine_type: Annotated[str, Field(example='бензин')]
    transmission: Annotated[str, Field(example='МКПП')]
    drive: Annotated[str, Field(example='полный привод (4WD)')]
