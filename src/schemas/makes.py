from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated


class MakeRead(BaseModel):
    """The model representing the vehicle make data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    created: datetime
    updated: datetime
    name: Annotated[str, Field(example='Renault')]
