from pydantic import BaseModel, Field
from typing import Annotated


class UnhandledDromResponseErrorRead(BaseModel):
    """The model describes the error that occurred when receiving a response from the drom.ru."""
    location: Annotated[str, Field(example='Марки')]
    request_url: Annotated[str, Field(example='https://www.drom.ru/catalog-unknown/')]
    response_status_code: Annotated[int, Field(example=404)]
    response_reason: Annotated[str, Field(example='Not Found')]


class UnhandledDromResponseErrorsRead(BaseModel):
    """The model describes the response to a request for data scraping from drom.ru."""
    unhandled_errors: list[UnhandledDromResponseErrorRead]


class ServiceFromEgrulEgripRead(BaseModel):
    """The model describes the vehicle service data that is scraped from the EGRUL or EGRIP by its INN."""
    name: Annotated[str, Field(example='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "РЕСУРС-А"')]
    ogrn: Annotated[str, Field(example='1237600011571')]
    is_working: bool
