import requests
import time
from bs4 import BeautifulSoup
from src.models.model import ModelTypeEnum
from src.configurations.model import EngineTypeEnum, TransmissionEnum, DriveEnum
from src.makes.repository import MakesRepository
from src.models.repository import ModelsRepository
from src.ranges.repository import RangesRepository
from src.generations.repository import GenerationsRepository
from src.configurations.repository import ConfigurationsRepository
from src.exceptions import UnhandledEgrulEgripResponseException, ServiceInnNotFoundInEgrulEgripException
from .schemas import UnhandledDromResponseErrorsRead, UnhandledDromResponseErrorRead, ServiceFromEgrulEgripRead


class DromScraperService:
    def __init__(
            self,
            makes_repository: MakesRepository,
            models_repository: ModelsRepository,
            ranges_repository: RangesRepository,
            generations_repository: GenerationsRepository,
            configurations_repository: ConfigurationsRepository
    ):
        self.makes_repository: MakesRepository = makes_repository
        self.models_repository: ModelsRepository = models_repository
        self.ranges_repository: RangesRepository = ranges_repository
        self.generations_repository: GenerationsRepository = generations_repository
        self.configurations_repository: ConfigurationsRepository = configurations_repository

    async def scrape_makes(self, url: str) -> list[UnhandledDromResponseErrorRead]:
        time.sleep(1.5)
        response = requests.get(url, allow_redirects=False)
        if response.status_code != 200:
            return [
                UnhandledDromResponseErrorRead(
                    location='Марки',
                    request_url=url,
                    response_status_code=response.status_code,
                    response_reason=response.reason
                )
            ]

        html = BeautifulSoup(response.text, 'html.parser')
        links = html.find_all('a', attrs={'data-ftid': 'component_cars-list-item_hidden-link'})
        links.extend(html.find_all('noscript')[1].find_all('a'))

        unhandled_errors = []
        for link in links:
            name = link.text
            res = await self.makes_repository.filter_by(name=name)
            make = await self.makes_repository.create({'name': name}) if not res else res[0]
            unhandled_errors += await self.scrape_models(make.id, link['href'])
        return unhandled_errors

    async def scrape_models(self, make_id: int, url: str) -> list[UnhandledDromResponseErrorRead]:
        time.sleep(1.5)
        response = requests.get(url, allow_redirects=False)
        if response.status_code != 200:
            return [
                UnhandledDromResponseErrorRead(
                    location='Модели',
                    request_url=url,
                    response_status_code=response.status_code,
                    response_reason=response.reason
                )
            ]

        _type = ModelTypeEnum.truck if url.startswith('https://www.drom.ru/catalog/lcv/') else ModelTypeEnum.passenger

        html = BeautifulSoup(response.text, 'html.parser')
        links = html.find_all('a', attrs={'data-ga-stats-name': 'model_from_list'})

        unhandled_errors = []
        for link in links:
            name = link.text
            res = await self.models_repository.filter_by(name=name, make_id=make_id)
            if not res:
                model = await self.models_repository.create({'name': name, 'type': _type, 'make_id': make_id})
            else:
                model = res[0]
            unhandled_errors += await self.scrape_ranges_and_generations(model.id, link['href'])
        return unhandled_errors

    async def scrape_ranges_and_generations(self, model_id: int, url: str) -> list[UnhandledDromResponseErrorRead]:
        time.sleep(1.5)
        response = requests.get(url, allow_redirects=False)
        if response.status_code != 200:
            return [
                UnhandledDromResponseErrorRead(
                    location='Модельные ряды и поколения',
                    request_url=url,
                    response_status_code=response.status_code,
                    response_reason=response.reason
                )
            ]

        html = BeautifulSoup(response.text, 'html.parser')
        range_name_divs = html.find_all('div', string=lambda text: text and 'Модельный ряд' in text)

        unhandled_errors = []
        for range_name_div in range_name_divs:
            name = range_name_div.text
            res = await self.ranges_repository.filter_by(name=name, model_id=model_id)
            _range = await self.ranges_repository.create({'name': name, 'model_id': model_id}) if not res else res[0]

            generation_divs = range_name_div.parent.find_all(
                'div', attrs={'data-ga-stats-name': 'generations_outlet_item'}
            )

            for generation_div in generation_divs:
                photo_url = generation_div.find('img')['src']
                full_name = generation_div.find(
                    'span', attrs={'data-ftid': 'component_article_caption'}
                ).find('span').text

                generation_info = generation_div.find(
                    'div', attrs={'data-ftid': 'component_article_extended-info'}
                ).find_all('div')
                short_name = generation_info[0].text
                vehicle_body = generation_info[-1].text

                res = await self.generations_repository.filter_by(photo_url=photo_url, range_id=_range.id)
                if not res:
                    generation = await self.generations_repository.create({
                        'photo_url': photo_url,
                        'full_name': full_name,
                        'short_name': short_name,
                        'vehicle_body': vehicle_body if ',' not in vehicle_body else vehicle_body.split(',')[0],
                        'range_id': _range.id
                    })
                else:
                    generation = res[0]
                unhandled_errors += await self.scrape_configurations(
                    generation.id, url + generation_div.find('a')['href']
                )

        return unhandled_errors

    async def scrape_configurations(self, generation_id: int, url: str) -> list[UnhandledDromResponseErrorRead]:
        time.sleep(1.5)
        response = requests.get(url, allow_redirects=False)
        if response.status_code != 200:
            return [
                UnhandledDromResponseErrorRead(
                    location='Конфигурации',
                    request_url=url,
                    response_status_code=response.status_code,
                    response_reason=response.reason
                )
            ]

        html = BeautifulSoup(response.text, 'html.parser')

        trs = html.find_all(
            'tr',
            attrs={'class': 'b-table__row b-table_align_top b-table__row_border_bottom b-table__row_padding_size-s'}
        )
        ths = []
        for i in range(1, len(trs)):
            ths += trs[i].find('th')

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
                    engine_power = int(elem.replace(' л.с.', ''))
                elif ' л' in elem:
                    engine_capacity = float(elem.replace(' л', ''))

            res = await self.configurations_repository.exists(
                engine_capacity=engine_capacity,
                engine_power=engine_power,
                engine_type=engine_type,
                transmission=transmission,
                drive=drive,
                generation_id=generation_id
            )

            if not res:
                await self.configurations_repository.create({
                    'engine_capacity': engine_capacity,
                    'engine_power': engine_power,
                    'engine_type': engine_type,
                    'transmission': transmission,
                    'drive': drive,
                    'generation_id': generation_id
                })
        return []

    async def init_scraper(self) -> UnhandledDromResponseErrorsRead:
        unhandled_errors = await self.scrape_makes('https://www.drom.ru/catalog/')
        unhandled_errors += await self.scrape_makes('https://www.drom.ru/catalog/lcv/')
        return UnhandledDromResponseErrorsRead(unhandled_errors=unhandled_errors)


class EgrulEgripScraperService:
    @staticmethod
    def scrape_name_and_ogrn(inn: str) -> ServiceFromEgrulEgripRead:
        base_url = 'https://egrul.nalog.ru'

        response = requests.post(base_url, data={'query': inn})
        if not 200 <= response.status_code <= 299 or not (token := response.json().get('t')):
            raise UnhandledEgrulEgripResponseException(detail='Ошибка при получении токена по ИНН.')

        search_url = f'{base_url}/search-result/{token}'
        response = requests.get(search_url)
        if not 200 <= response.status_code <= 299 or not (records := response.json().get('rows')):
            raise UnhandledEgrulEgripResponseException(
                detail='Ошибка при получении списка записей из ЕГРЮЛ или ЕГРИП по токену.'
            )

        if len(records) == 0 or not (fresh_record := records[0]).get('n'):
            raise ServiceInnNotFoundInEgrulEgripException()

        return ServiceFromEgrulEgripRead(
            name=fresh_record['n'],
            ogrn=fresh_record['o'],
            is_working=True if 'e' not in fresh_record else False
        )

