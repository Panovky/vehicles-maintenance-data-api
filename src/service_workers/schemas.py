from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated
from src.users.schemas import UserRead


class ServiceWorkerInvite(BaseModel):
    """The model representing the service worker data needed to send email to attach worker to service."""
    email: Annotated[EmailStr, Field(example='nikita.filatov@yandex.ru')]
    position: Annotated[str, Field(max_length=100, example='Специалист по кузовному ремонту')]


class ServiceWorkerRead(BaseModel):
    """The model representing the service worker data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    last_name: Annotated[str, Field(example='Ягодкин')]
    first_name: Annotated[str, Field(example='Вячеслав')]
    patronymic: Annotated[str | None, Field(example='Андреевич')]
    photo_path: Annotated[str, Field(example='/static/users/photos/46.jpg')]
    phone: Annotated[str | None, Field(example='+7 (999) 777-33-11')]
    email: Annotated[EmailStr, Field(example='yava@yandex.ru')]
    position: Annotated[str, Field(example='Специалист по кузовному ремонту')]
    rating: Annotated[float, Field(example=4.7)]
