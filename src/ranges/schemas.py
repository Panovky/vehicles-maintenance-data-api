from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class RangeRead(BaseModel):
    """The model representing the vehicles model range data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    name: Annotated[str, Field(example='Модельный ряд Renault Duster для России')]
    model_id: Annotated[int, Field(example=1)]
