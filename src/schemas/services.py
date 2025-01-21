from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated


class ServiceRead(BaseModel):
    """The model representing the service data to be returned to the client."""
    id: Annotated[int, Field(example=1)]
    created: datetime
    updated: datetime
    name: Annotated[str, Field(example='LeCar Service')]
    address: Annotated[str, Field(example='г. Ярославль, р-н Красноперекопский, Московский проспект, д. 110, к. Б')]
    summary: Annotated[str | None, Field(example='Сервис по ремонту авто любой сложности.')]
    timetable: Annotated[str, Field(example='Ежедневно с 08:00 до 20:00')]
    website: Annotated[str | None, Field(example='https://yaroslavl.lecar.ru/')]


class ServiceCreate(BaseModel):
    """The model representing the service data needed to create record in the database."""
    name: Annotated[str, Field(max_length=255, example='LeCar Service')]
    address: Annotated[str, Field(
        max_length=255, example='г. Ярославль, р-н Красноперекопский, Московский проспект, д. 110, к. Б'
    )]
    summary: Annotated[str | None, Field(
        max_length=500, default=None, example='Сервис по ремонту авто любой сложности.'
    )]
    timetable: Annotated[str, Field(max_length=255, example='Ежедневно с 08:00 до 20:00')]
    website: Annotated[str | None, Field(max_length=255, default=None, example='https://yaroslavl.lecar.ru/')]


class ServiceUpdate(BaseModel):
    """The model representing the service data needed to update information in the database."""
    name: Annotated[str | None, Field(max_length=255, default=None, example='LeCar Service')]
    address: Annotated[str | None, Field(
        max_length=255, default=None, example='г. Ярославль, р-н Красноперекопский, Московский проспект, д. 110, к. Б'
    )]
    summary: Annotated[str | None, Field(
        max_length=500, default=None, example='Сервис по ремонту авто любой сложности.'
    )]
    timetable: Annotated[str | None, Field(max_length=255, default=None, example='Ежедневно с 08:00 до 20:00')]
    website: Annotated[str | None, Field(max_length=255, default=None, example='https://yaroslavl.lecar.ru/')]
