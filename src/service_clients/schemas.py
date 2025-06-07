from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated


class ServiceClientRead(BaseModel):
    """The model representing the service client data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    last_name: Annotated[str, Field(example='Ягодкина')]
    first_name: Annotated[str, Field(example='Кристина')]
    patronymic: Annotated[str | None, Field(example='Олеговна')]
    photo_path: Annotated[str, Field(example='/static/users/photos/3f9c7b4a8e8d4a5d9e1b0c7a3d8f2e1a.jpg')]
    phone: Annotated[str | None, Field(example='+7 (901) 999-99-99')]
    email: Annotated[EmailStr, Field(example='yakro@yandex.ru')]