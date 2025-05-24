from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from .model import UserRoleEnum


class UserRoleCreate(BaseModel):
    """The model representing the data needed to assign a new role to the current user."""
    role: UserRoleEnum


class UserRoleRead(BaseModel):
    """The model representing the user role data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    user_id: Annotated[int, Field(example=1)]
    role: UserRoleEnum
