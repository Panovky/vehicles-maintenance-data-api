import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select
from src.dependencies import SessionDep
from src.models import Make, Model
from src.schemas import ScrapeResponse
from src.services.scrape import scrape_makes, scrape_models, UnexpectedDromResponseError


router = APIRouter(
    prefix='/scrape',
    tags=['scrape']
)


@router.post('/', responses={200: {'model': ScrapeResponse}}, summary='Scrape drom.ru')
def scrape_drom_ru(session: SessionDep) -> JSONResponse:
    """
    Scrape vehicles makes, models, models ranges, generations and configurations from drom.ru.

    Field detail in a response either indicates whether the data is successfully scraped or where the script failed.

    If there was an error when receiving the response from drom.ru,
    the drom_response_status_code field will be used to return the status code of the response from drom.ru.
    """
    try:
        scraped_makes = scrape_makes('https://www.drom.ru/catalog') + scrape_makes('https://www.drom.ru/catalog/lcv')
    except UnexpectedDromResponseError as e:
        return JSONResponse(content={'detail': e.detail, 'drom_response_status_code': e.drom_response_status_code})

    for scraped_make in scraped_makes:
        if scraped_make.name not in session.execute(select(Make.name)).scalars():
            make = Make(name=scraped_make.name)
            session.add(make)
            session.commit()

        try:
            scrapped_models = scrape_models(scraped_make.models_drom_url)
        except UnexpectedDromResponseError as e:
            return JSONResponse(content={'detail': e.detail, 'drom_response_status_code': e.drom_response_status_code})

        make_id = session.execute(select(Make.id).where(Make.name == scraped_make.name)).scalar()

        for scraped_model in scrapped_models:
            if scraped_model.name not in session.execute(select(Model.name).where(Model.make_id == make_id)).scalars():
                model = Model(name=scraped_model.name, type=scraped_model.type, make_id=make_id)
                session.add(model)
                session.commit()
        time.sleep(1.5)

    return JSONResponse(content={'detail': 'Data from drom.ru successfully scraped.'})
