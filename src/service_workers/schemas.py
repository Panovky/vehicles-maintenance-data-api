from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class ServiceWorkerInvite(BaseModel):
    """The model representing the worker data needed to send email to attach worker to service."""
    email: Annotated[EmailStr, Field(example='nikita.filatov@yandex.ru')]
    position: Annotated[str, Field(max_length=100, example='Специалист по кузовному ремонту')]
