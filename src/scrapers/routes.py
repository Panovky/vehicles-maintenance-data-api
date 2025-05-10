from fastapi import APIRouter, Body
from typing import Annotated
from src.dependencies import CurrentAdminDep, CurrentManagerDep, DromScraperServiceDep, EgrulEgripScraperServiceDep
from .schemas import UnhandledDromResponseErrorsRead, ServiceFromEgrulEgripRead

router = APIRouter(
    prefix='/scrapers',
    tags=['scrapers']
)


@router.post(
    '/drom',
    responses={
        200: {'description': 'Data successfully scraped'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Scrape data from drom.ru'
)
async def scrape_drom_data(
        current_admin: CurrentAdminDep, drom_scraper_service: DromScraperServiceDep
) -> UnhandledDromResponseErrorsRead:
    return await drom_scraper_service.init_scraper()


@router.post(
    '/egrul-egrip',
    responses={
        200: {'description': 'Data successfully scraped'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Records in EGRUL and EGRIP not found'},
        424: {'description': 'Error on the external service side'}
    },
    summary='Scrape data from EGRUL and EGRIP'
)
def scrape_egrul_egrip_data(
        current_manager: CurrentManagerDep,
        inn: Annotated[str, Body(pattern=r'^\d{10}$|^\d{12}$', embed=True)],
        egrul_egrip_scraper_service: EgrulEgripScraperServiceDep
) -> ServiceFromEgrulEgripRead:
    return egrul_egrip_scraper_service.scrape_name_and_ogrn(inn)
