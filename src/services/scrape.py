import requests
from bs4 import BeautifulSoup
from src.models import ModelTypeEnum
from src.schemas import MakeScrape, ModelScrape


def scrape_makes(makes_drom_url) -> list[MakeScrape]:
    """Return a list of all vehicle makes scrapped from specified url in drom.ru."""

    links = []
    response = requests.get(makes_drom_url)
    if response.status_code == 200:
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
    """Return a list of all vehicle models scrapped from specified url in drom.ru."""

    if models_drom_url.startswith('https://www.drom.ru/catalog/lcv/'):
        _type = ModelTypeEnum.truck
    else:
        _type = ModelTypeEnum.passenger

    links = []
    response = requests.get(models_drom_url)
    if response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')
        links = html.find_all('a', attrs={'data-ga-stats-name': 'model_from_list'})

    models = []
    for link in links:
        name = link.text
        ranges_drom_url = link['href']
        model = ModelScrape(name=name, type=_type, ranges_drom_url=ranges_drom_url)
        models.append(model)

    return models
