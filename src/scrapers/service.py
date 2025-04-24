import requests
from bs4 import BeautifulSoup
from src.models.model import ModelTypeEnum
from src.configurations.model import EngineTypeEnum, TransmissionEnum, DriveEnum
from src.makes.repository import MakesRepository
from src.models.repository import ModelsRepository
from src.ranges.repository import RangesRepository
from src.generations.repository import GenerationsRepository
from src.configurations.repository import ConfigurationsRepository
from .schemas import MakeScrape, ModelScrape, RangeScrape, GenerationScrape, ConfigurationScrape


class DromScraperService:
    def __init__(
            self, makes_repository: MakesRepository, models_repository: ModelsRepository,
            ranges_repository: RangesRepository, generations_repository: GenerationsRepository,
            configurations_repository: ConfigurationsRepository
    ):
        self.makes_repository: MakesRepository = makes_repository
        self.models_repository: ModelsRepository = models_repository
        self.ranges_repository: RangesRepository = ranges_repository
        self.generations_repository: GenerationsRepository = generations_repository
        self.configurations_repository: ConfigurationsRepository = configurations_repository


class UnexpectedDromResponseError(Exception):
    location: str
    drom_request_url: str
    drom_response_status_code: int
    drom_response_reason: str

    def __init__(self, location, drom_request_url, drom_response_status_code, drom_response_reason):
        super().__init__()
        self.location = location
        self.drom_request_url = drom_request_url
        self.drom_response_status_code = drom_response_status_code
        self.drom_response_reason = drom_response_reason


def scrape_makes(makes_drom_url: str) -> list[MakeScrape]:
    """Return a list of all vehicle makes scraped from specified url in drom.ru."""

    response = requests.get(makes_drom_url, allow_redirects=False)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping makes.',
            makes_drom_url,
            response.status_code,
            response.reason
        )

    html = BeautifulSoup(response.text, 'html.parser')
    links = html.find_all('a', attrs={'data-ftid': 'component_cars-list-item_hidden-link'})
    links.extend(html.find_all('noscript')[1].find_all('a'))

    makes = []
    for link in links:
        make = MakeScrape(name=link.text, models_drom_url=link['href'])
        makes.append(make)

    return makes


def scrape_models(models_drom_url: str) -> list[ModelScrape]:
    """Return a list of all vehicle models scraped from specified url in drom.ru."""

    response = requests.get(models_drom_url, allow_redirects=False)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping models.',
            models_drom_url,
            response.status_code,
            response.reason
        )

    html = BeautifulSoup(response.text, 'html.parser')
    links = html.find_all('a', attrs={'data-ga-stats-name': 'model_from_list'})

    if models_drom_url.startswith('https://www.drom.ru/catalog/lcv/'):
        _type = ModelTypeEnum.truck
    else:
        _type = ModelTypeEnum.passenger

    models = []
    for link in links:
        model = ModelScrape(name=link.text, type=_type, ranges_and_generations_drom_url=link['href'])
        models.append(model)

    return models


def scrape_ranges_and_generations(ranges_and_generations_drom_url: str) -> list[RangeScrape]:
    """Return a list of all vehicles models ranges with them generations list scraped from specified url in drom.ru."""

    response = requests.get(ranges_and_generations_drom_url, allow_redirects=False)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping models ranges and generations.',
            ranges_and_generations_drom_url,
            response.status_code,
            response.reason
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

            generation_info = generation_div.find(
                'div', attrs={'data-ftid': 'component_article_extended-info'}).find_all('div')
            short_name = generation_info[0].text
            vehicle_body = generation_info[-1].text

            configurations_drom_url = ranges_and_generations_drom_url + generation_div.find('a')['href']

            generation = GenerationScrape(
                photo_url=photo_url,
                full_name=full_name,
                short_name=short_name,
                vehicle_body=vehicle_body if ',' not in vehicle_body else vehicle_body.split(',')[0],
                configurations_drom_url=configurations_drom_url
            )
            generations.append(generation)

        _range = RangeScrape(name=range_name, generations=generations)
        ranges.append(_range)

    return ranges


def scrape_configurations(configurations_drom_url: str) -> list[ConfigurationScrape]:
    """Return a list of all vehicle configurations scraped from specified url in drom.ru."""

    response = requests.get(configurations_drom_url, allow_redirects=False)
    if response.status_code != 200:
        raise UnexpectedDromResponseError(
            'Unexpected drom.ru response error occurred while scraping configurations.',
            configurations_drom_url,
            response.status_code,
            response.reason
        )

    html = BeautifulSoup(response.text, 'html.parser')
    trs = html.find_all('tr', attrs={
        'class': 'b-table__row b-table_align_top b-table__row_border_bottom b-table__row_padding_size-s'
    })
    ths = []
    for i in range(1, len(trs)):
        ths += trs[i].find('th')

    configurations = []
    for th in ths:
        configuration_info = th.text

        engine_type = None
        for elem in EngineTypeEnum:
            if (value := elem.value) in configuration_info:
                engine_type = value
                break

        transmission = None
        for elem in TransmissionEnum:
            if (value := elem.value) in configuration_info:
                transmission = value
                break

        drive = None
        for elem in DriveEnum:
            if (value := elem.value) in configuration_info:
                drive = value
                break

        engine_capacity = None
        engine_power = None
        configuration_info_list = configuration_info.split(',')
        for elem in configuration_info_list:
            if ' л.с.' in elem:
                engine_power = elem.replace(' л.с.', '')
            elif ' л' in elem:
                engine_capacity = elem.replace(' л', '')

        configuration = ConfigurationScrape(
            engine_capacity=engine_capacity,
            engine_power=engine_power,
            engine_type=engine_type,
            transmission=transmission,
            drive=drive
        )

        configurations.append(configuration)

    return configurations


def get_unhandled_error_info(e: UnexpectedDromResponseError) -> dict[str, str | int]:
    """Return a dictionary with data about the error that occurred when receiving a response from the drom.ru."""
    return {
        'location': e.location,
        'drom_request_url': e.drom_request_url,
        'drom_response_status_code': e.drom_response_status_code,
        'drom_response_reason': e.drom_response_reason
    }
