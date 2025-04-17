from datetime import date
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class UserRegister(BaseModel):
    """The model representing the data needed to register the user."""
    last_name: Annotated[str, Field(max_length=100, example="Филатов")]
    first_name: Annotated[str, Field(max_length=50, example="Никита")]
    patronymic: Annotated[str | None, Field(max_length=40, default=None, example="Андреевич")]
    birthday: Annotated[date | None, Field(example="1984-09-05")]
    phone: Annotated[str | None, Field(pattern=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$', example="+7 (950) 732-13-83")]
    email: Annotated[EmailStr, Field(example="nikita.filatov@yandex.ru")]
    password: Annotated[str, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', example="2a_B4-cJ_q5")]
    role_id: Annotated[int, Field(example=1)]


class UserLogin(BaseModel):
    """The model representing the data needed to log in the user."""
    email: Annotated[EmailStr, Field(example="nikita.filatov@yandex.ru")]
    password: Annotated[str, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', example="2a_B4-cJ_q5")]


class AccessTokenRead(BaseModel):
    """The model representing the token data to be returned to the client."""
    access_token: str
    token_type: str
