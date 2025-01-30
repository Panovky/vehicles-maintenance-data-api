from pydantic import BaseModel, Field
from typing import Annotated


class ConfigurationRead(BaseModel):
    """The model representing the vehicle configuration data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    engine_capacity: Annotated[float, Field(example='1.3')]
    engine_power: Annotated[int, Field(example='149')]
    engine_type: Annotated[str, Field(example='бензин')]
    transmission: Annotated[str, Field(example='МКПП')]
    drive: Annotated[str, Field(example='полный привод (4WD)')]
