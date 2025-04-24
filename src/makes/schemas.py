from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class MakeCreate(BaseModel):
    """The model representing the vehicle make data needed to create record in the database."""
    name: Annotated[str, Field(max_length=40, example='Renault')]


class MakeRead(BaseModel):
    """The model representing the vehicle make data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    name: Annotated[str, Field(example='Renault')]
