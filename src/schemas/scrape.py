from pydantic import BaseModel, Field
from typing import Annotated
from src.models import ModelTypeEnum


class MakeScrape(BaseModel):
    """
    The model representing the data of vehicle make scraped from drom.ru.

    The model used for further data scraping.
    """
    name: str
    models_drom_url: str


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


class ScrapeResponse(BaseModel):
    """The model describes the response to a request for data scraping from drom.ru."""
    detail: Annotated[str, Field(example='Unexpected drom.ru response error occurred while scraping models.')]
    drom_reponse_status_code: Annotated[int | None, Field(example=404)]
