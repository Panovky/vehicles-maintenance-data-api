from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated
from src.user_roles.model import UserRoleEnum


class UserRead(BaseModel):
    """The model representing the user data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    last_name: Annotated[str, Field(example="Филатов")]
    first_name: Annotated[str, Field(example="Никита")]
    patronymic: Annotated[str | None, Field(example="Андреевич")]
    photo_path: Annotated[str, Field(example='/static/users/photos/nikita.filatov@yandex.ru.jpg')]
    birthday: Annotated[date | None, Field(example="1984-09-05")]
    phone: Annotated[str | None, Field(example="+7 (950) 732-13-83")]
    email: Annotated[EmailStr, Field(example="nikita.filatov@yandex.ru")]
    roles: list[UserRoleEnum]


class UserUpdate(BaseModel):
    """The model representing the user data needed to update information in the database."""
    last_name: Annotated[str | None, Field(max_length=100, default=None, example="Филатов")]
    first_name: Annotated[str | None, Field(max_length=50, default=None, example="Никита")]
    patronymic: Annotated[str | None, Field(max_length=40, default=None, example="Андреевич")]
    birthday: Annotated[str | None, Field(default=None, example="1984-09-05")]
    phone: Annotated[str | None, Field(pattern=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}|$', default=None,
                                       example="+7 (950) 732-13-83")]
