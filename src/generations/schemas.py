from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class GenerationRead(BaseModel):
    """The model representing the vehicle generation data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    photo_url: Annotated[str, Field(example='https://www.drom.ru/catalog/renault/duster/g_2020_12623/')]
    full_name: Annotated[str, Field(example='Renault Duster (HM)\n11.2020 - 07.2022')]
    short_name: Annotated[str, Field(example='2 поколение')]
    vehicle_body: Annotated[str, Field(example='Джип/SUV 5 дв.')]
    range_id: Annotated[int, Field(example=1)]
