from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class ServiceRead(BaseModel):
    """The model representing the service data to be returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(example=1)]
    created_at: datetime
    updated_at: datetime
    name: Annotated[str, Field(example='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "РЕСУРС-А"')]
    inn: Annotated[str, Field(example='7604394801')]
    ogrn: Annotated[str, Field(example='1237600011571')]
    address: Annotated[str, Field(example='Ярославская область, г. Ярославль, ул. Нефтяников, 17А')]
    summary: Annotated[str | None, Field(example='Сервис по ремонту авто любой сложности.')]
    timetable: Annotated[str, Field(example='Пн-Пт - 8:00-20:00\nСб, Вс - 9:00-18:00\nРаботаем без выходных')]
    website: Annotated[str | None, Field(example='https://bestway76.ru/')]
    manager_id: Annotated[int, Field(example=1)]


class ServiceCreate(BaseModel):
    """The model representing the service data needed to create record in the database."""
    name: Annotated[str, Field(max_length=255, example='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "РЕСУРС-А"')]
    inn: Annotated[str, Field(example='7604394801')]
    ogrn: Annotated[str, Field(example='1237600011571')]
    address: Annotated[str, Field(max_length=255, example='Ярославская область, г. Ярославль, ул. Нефтяников, 17А')]
    summary: Annotated[
        str | None,
        Field(max_length=500, default=None, example='Сервис по ремонту авто любой сложности.')
    ]
    timetable: Annotated[
        str,
        Field(max_length=255, example='Пн-Пт - 8:00-20:00 Сб, Вс - 9:00-18:00 Работаем без выходных')
    ]
    website: Annotated[str | None, Field(max_length=255, default=None, example='https://bestway76.ru/')]
