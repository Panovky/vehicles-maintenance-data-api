from pydantic import BaseModel


class MakeScrape(BaseModel):
    """
    The model representing the data of vehicle make scrapped from drom.ru.

    The model used for further data scrapping.
    """
    name: str
    models_drom_url: str


class ModelScrape(BaseModel):
    """
    The model representing the data of vehicle model scrapped from drom.ru.

    The model used for further data scrapping.
    """
    name: str
    ranges_drom_url: str
