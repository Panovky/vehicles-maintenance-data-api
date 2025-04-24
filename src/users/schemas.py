from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated
from .model import RoleEnum


class UserRoleCreate(BaseModel):
    """The model representing the data needed to assign a new role to the current user."""
    role: RoleEnum


class UserRoleRead(BaseModel):
    """The model representing the user role data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    user_id: Annotated[int, Field(example=1)]
    role: RoleEnum


class UserRead(BaseModel):
    """The model representing the user data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    last_name: Annotated[str, Field(example="Филатов")]
    first_name: Annotated[str, Field(example="Никита")]
    patronymic: Annotated[str | None, Field(example="Андреевич")]
    birthday: Annotated[date | None, Field(example="1984-09-05")]
    phone: Annotated[str | None, Field(example="+7 (950) 732-13-83")]
    email: Annotated[EmailStr, Field(example="nikita.filatov@yandex.ru")]
    roles: list[RoleEnum]


class UserUpdate(BaseModel):
    """The model representing the user data needed to update information in the database."""
    last_name: Annotated[str | None, Field(max_length=100, default=None, example="Филатов")]
    first_name: Annotated[str | None, Field(max_length=50, default=None, example="Никита")]
    patronymic: Annotated[str | None, Field(max_length=40, default=None, example="Андреевич")]
    birthday: Annotated[str | None, Field(default=None, example="1984-09-05")]
    phone: Annotated[str | None, Field(pattern=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}|$', default=None,
                                       example="+7 (950) 732-13-83")]
