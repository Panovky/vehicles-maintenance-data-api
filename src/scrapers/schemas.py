from pydantic import BaseModel, Field
from typing import Annotated
from src.models.model import ModelTypeEnum


class ModelScrape(BaseModel):
    """
    The model representing the data of vehicle model scraped from drom.ru.

    The model used for further data scraping.
    """
    name: str
    type: ModelTypeEnum
    ranges_and_generations_drom_url: str


class GenerationScrape(BaseModel):
    """
    The model representing the data of vehicle generation scraped from drom.ru.

    The model used for further data scraping.
    """
    photo_url: str
    full_name: str
    short_name: str
    vehicle_body: str
    configurations_drom_url: str


class RangeScrape(BaseModel):
    """
    The model representing the data of vehicle models range scraped from drom.ru.

    The model used for further data scraping.
    """
    name: str
    generations: list[GenerationScrape]


class ConfigurationScrape(BaseModel):
    """
    The model representing the data of vehicle configurations scraped from drom.ru.

    The model used for further data scraping.
    """
    engine_capacity: float | None
    engine_power: int | None
    engine_type: str | None
    transmission: str | None
    drive: str | None


class UnhandledDromResponseErrorRead(BaseModel):
    """The model describes the error that occurred when receiving a response from the drom.ru."""
    location: Annotated[str, Field(example='Марки')]
    request_url: Annotated[str, Field(example='https://www.drom.ru/catalog-unknown/')]
    response_status_code: Annotated[int, Field(example=404)]
    response_reason: Annotated[str, Field(example='Not Found')]


class UnhandledDromResponseErrorsRead(BaseModel):
    """The model describes the list of errors that occurred when receiving a response from the drom.ru."""
    unhandled_errors: list[UnhandledDromResponseErrorRead]
