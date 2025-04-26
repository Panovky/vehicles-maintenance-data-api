from fastapi import APIRouter
from src.dependencies import CurrentAdminDep, DromScraperServiceDep
from .schemas import UnhandledDromResponseErrorsRead

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
