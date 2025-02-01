import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select, and_
from src.dependencies import SessionDep
from src.models import Make, Model, Range, Generation
from src.schemas import ScrapeResponse
from src.services.scrape import scrape_makes, scrape_models, scrape_ranges_and_generations, UnexpectedDromResponseError


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
        scraped_makes = scrape_makes('https://www.drom.ru/catalog')
        time.sleep(1.5)
        scraped_makes += scrape_makes('https://www.drom.ru/catalog/lcv')
        time.sleep(1.5)
        for scraped_make in scraped_makes:
            if scraped_make.name not in session.execute(select(Make.name)).scalars():
                make = Make(name=scraped_make.name)
                session.add(make)
                session.commit()

            scraped_models = scrape_models(scraped_make.models_drom_url)
            time.sleep(1.5)
            make_id = session.execute(select(Make.id).where(Make.name == scraped_make.name)).scalar()
            for scraped_model in scraped_models:
                if scraped_model.name not in session.execute(
                        select(Model.name)
                        .where(Model.make_id == make_id)
                ).scalars():
                    model = Model(name=scraped_model.name, type=scraped_model.type, make_id=make_id)
                    session.add(model)
                    session.commit()

                scraped_ranges = scrape_ranges_and_generations(scraped_model.ranges_and_generations_drom_url)
                time.sleep(1.5)
                model_id = session.execute(
                    select(Model.id)
                    .where(and_(Model.make_id == make_id, Model.name == scraped_model.name))
                ).scalar()
                for scraped_range in scraped_ranges:
                    if scraped_range.name not in session.execute(
                            select(Range.name)
                            .where(Range.model_id == model_id)
                    ).scalars():
                        _range = Range(name=scraped_range.name, model_id=model_id)
                        session.add(_range)
                        session.commit()

                    scraped_generations = scraped_range.generations
                    range_id = session.execute(
                        select(Range.id)
                        .where(and_(Range.model_id == model_id, Range.name == scraped_range.name))
                    ).scalar()
                    for scraped_generation in scraped_generations:
                        if scraped_generation.photo_url not in session.execute(
                                select(Generation.photo_url)
                                .where(Generation.range_id == range_id)
                        ).scalars():
                            generation = Generation(
                                photo_url=scraped_generation.photo_url,
                                full_name=scraped_generation.full_name,
                                short_name=scraped_generation.short_name,
                                vehicle_body=scraped_generation.vehicle_body,
                                range_id=range_id
                            )
                            session.add(generation)
                            session.commit()

    except UnexpectedDromResponseError as e:
        return JSONResponse(content={'detail': e.detail, 'drom_response_status_code': e.drom_response_status_code})

    return JSONResponse(content={'detail': 'Data from drom.ru successfully scraped.'})
