from pydantic import BaseModel, Field
from typing import Annotated


class GenerationRead(BaseModel):
    """The model representing the vehicle generation data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    photo_url: Annotated[str, Field(example='https://www.drom.ru/catalog/renault/duster/g_2020_12623/')]
    full_name: Annotated[str, Field(example='Renault Duster (HM)\n11.2020 - 07.2022')]
    short_name: Annotated[str, Field(example='2 поколение')]
    vehicle_body: Annotated[str, Field(example='Джип/SUV 5 дв.')]
    range_id: Annotated[int, Field(example=1)]
