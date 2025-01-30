from pydantic import BaseModel


class MakeScrape(BaseModel):
    """
    The model representing the data of vehicle make scrapped from drom.ru.

    id value is filled in after the vehicle make is added into the database.
    The model used for further data scrapping.
    """
    id: int | None = None
    name: str
    drom_url: str
