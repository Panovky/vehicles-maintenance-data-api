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
