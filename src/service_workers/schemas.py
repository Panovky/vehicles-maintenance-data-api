from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from src.users.schemas import UserRead


class ServiceWorkerInvite(BaseModel):
    """The model representing the service worker data needed to send email to attach worker to service."""
    email: Annotated[EmailStr, Field(example='nikita.filatov@yandex.ru')]
    position: Annotated[str, Field(max_length=100, example='Специалист по кузовному ремонту')]


class ServiceWorkerRead(UserRead):
    """The model representing the service worker data to be returned to the client."""
    position: Annotated[str, Field(example='Специалист по кузовному ремонту')]
    rating: Annotated[float, Field(example=4.7)]
