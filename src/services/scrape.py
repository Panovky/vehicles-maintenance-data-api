import requests
from bs4 import BeautifulSoup
from src.schemas import MakeScrape


def scrape_makes(url) -> list[MakeScrape]:
    """Return a list of all vehicle makes scrapped from specified url in drom.ru."""

    links = []
    response = requests.get(url)
    if response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')
        links = html.find_all('a', attrs={'data-ftid': 'component_cars-list-item_hidden-link'})
        links.extend(html.find_all('noscript')[1].find_all('a'))

    makes = []
    for link in links:
        name = link.text
        drom_url = link['href'].replace('https://www.drom.ru/catalog/', '')
        make = MakeScrape(name=name, drom_url=drom_url)
        makes.append(make)

    return makes
