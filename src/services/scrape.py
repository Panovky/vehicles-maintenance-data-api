import requests
from bs4 import BeautifulSoup
from src.models import ModelTypeEnum
from src.schemas import MakeScrape, ModelScrape, RangeScrape, GenerationScrape


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
        ranges_and_generations_drom_url = link['href']
        model = ModelScrape(name=name, type=_type, ranges_and_generations_drom_url=ranges_and_generations_drom_url)
        models.append(model)

    return models


def scrape_ranges_and_generations(ranges_and_generations_drom_url) -> list[RangeScrape]:
    """Return a list of all vehicles models ranges with them generations list scraped from specified url in drom.ru."""

    response = requests.get(ranges_and_generations_drom_url)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping models ranges and generations.',
            response.status_code
        )

    html = BeautifulSoup(response.text, 'html.parser')
    range_name_divs = html.find_all('div', string=lambda text: text and 'Модельный ряд' in text)

    ranges = []
    for range_name_div in range_name_divs:
        range_name = range_name_div.text
        generation_divs = range_name_div.parent.find_all('div', attrs={'data-ga-stats-name': 'generations_outlet_item'})

        generations = []
        for generation_div in generation_divs:
            photo_url = generation_div.find('img')['src']
            full_name = generation_div.find('span', attrs={'data-ftid': 'component_article_caption'}).find('span').text
            generation_info = generation_div.find('div', attrs={'data-ftid': 'component_article_extended-info'}).find_all('div')
            short_name = generation_info[0].text
            vehicle_body = generation_info[-1].text
            configurations_drom_url = generation_div.find('a')['href']
            generation = GenerationScrape(
                photo_url=photo_url,
                full_name=full_name,
                short_name=short_name,
                vehicle_body=vehicle_body,
                configurations_drom_url=configurations_drom_url
            )
            generations.append(generation)
        _range = RangeScrape(name=range_name, generations=generations)
        ranges.append(_range)

    return ranges
