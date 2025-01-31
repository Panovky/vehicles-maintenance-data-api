import requests
from bs4 import BeautifulSoup
from src.models import ModelTypeEnum
from src.schemas import MakeScrape, ModelScrape


class UnexpectedDromResponseError(Exception):
    detail: str
    drom_response_status_code: int

    def __init__(self, detail, drom_response_status_code):
        super().__init__()
        self.detail = detail
        self.drom_response_status_code = drom_response_status_code


def scrape_makes(makes_drom_url) -> list[MakeScrape]:
    """Return a list of all vehicle makes scraped from specified url in drom.ru."""

    response = requests.get(makes_drom_url)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping makes.',
            response.status_code
        )

    html = BeautifulSoup(response.text, 'html.parser')
    links = html.find_all('a', attrs={'data-ftid': 'component_cars-list-item_hidden-link'})
    links.extend(html.find_all('noscript')[1].find_all('a'))

    makes = []
    for link in links:
        name = link.text
        models_drom_url = link['href']
        make = MakeScrape(name=name, models_drom_url=models_drom_url)
        makes.append(make)

    return makes


def scrape_models(models_drom_url) -> list[ModelScrape]:
    """Return a list of all vehicle models scraped from specified url in drom.ru."""

    response = requests.get(models_drom_url)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping models.',
            response.status_code
        )

    html = BeautifulSoup(response.text, 'html.parser')
    links = html.find_all('a', attrs={'data-ga-stats-name': 'model_from_list'})

    if models_drom_url.startswith('https://www.drom.ru/catalog/lcv/'):
        _type = ModelTypeEnum.truck
    else:
        _type = ModelTypeEnum.passenger

    models = []
    for link in links:
        name = link.text
        ranges_drom_url = link['href']
        model = ModelScrape(name=name, type=_type, ranges_drom_url=ranges_drom_url)
        models.append(model)

    return models
