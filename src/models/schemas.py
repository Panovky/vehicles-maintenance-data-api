from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated
from src.entities import ModelTypeEnum


class ModelRead(BaseModel):
    """The model representing the vehicle model data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    name: Annotated[str, Field(example='Duster')]
    type: ModelTypeEnum
    make_id: Annotated[int, Field(example=1)]
