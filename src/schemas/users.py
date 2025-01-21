from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated
from src.models.user import UserRoleEnum


def validate_birthday(birthday: date) -> date:
    today_date = date.today()
    eighteen_years_ago_date = date(today_date.year - 18, today_date.month, today_date.day)
    if birthday > eighteen_years_ago_date:
        raise ValueError('User must be at least 18 years old.')
    return birthday


class UserRead(BaseModel):
    """The model representing the user data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    created: datetime
    updated: datetime
    last_name: Annotated[str, Field(example="Филатов")]
    first_name: Annotated[str, Field(example="Никита")]
    patronymic: Annotated[str | None, Field(example="Андреевич")]
    birthday: Annotated[date, Field(example="1984-09-05")]
    phone: Annotated[str, Field(example="+7 (950) 732-13-83")]
    email: Annotated[str, Field(example="nikita.filatov@yandex.ru")]
    role: UserRoleEnum
    login: Annotated[str, Field(example="zz_filin_zz")]


class UserCreate(BaseModel):
    """The model representing the user data needed to create record in the database."""
    last_name: Annotated[str, Field(max_length=100, example="Филатов")]
    first_name: Annotated[str, Field(max_length=50, example="Никита")]
    patronymic: Annotated[str | None, Field(max_length=40, default=None, example="Андреевич")]
    birthday: Annotated[date, Field(example="1984-09-05")]
    phone: Annotated[str, Field(pattern=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$', example="+7 (950) 732-13-83")]
    email: Annotated[EmailStr, Field(example="nikita.filatov@yandex.ru")]
    role: UserRoleEnum
    login: Annotated[str, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', example="zz_filin_zz")]
    password: Annotated[str, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', example="2a_B4-cJ_q5")]

    _validate_birthday = field_validator('birthday')(validate_birthday)


class UserUpdate(BaseModel):
    """The model representing the user data needed to update information in the database."""
    last_name: Annotated[str | None, Field(max_length=100, default=None, example="Филатов")]
    first_name: Annotated[str | None, Field(max_length=50, default=None, example="Никита")]
    patronymic: Annotated[str | None, Field(max_length=40, default=None, example="Андреевич")]
    birthday: Annotated[date | None, Field(default=None, example="1984-09-05")]
    phone: Annotated[str | None, Field(pattern=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$', default=None,
                                       example="+7 (950) 732-13-83")]
    email: Annotated[EmailStr | None, Field(default=None, example="nikita.filatov@yandex.ru")]
    role: Annotated[UserRoleEnum | None, Field(default=None)]
    login: Annotated[str | None, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', default=None, example="zz_filin_zz")]
    password: Annotated[str | None, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', default=None, example="2a_B4-cJ_q5")]

    _validate_birthday = field_validator('birthday')(validate_birthday)
