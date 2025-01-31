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
    ranges_drom_url: str


class ScrapeResponse(BaseModel):
    """The model describes the response to a request for data scraping from drom.ru."""
    detail: Annotated[str, Field(example='Unexpected drom.ru response error occurred while scraping models.')]
    drom_reponse_status_code: Annotated[int | None, Field(example=404)]
