import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select, and_, exists
from src.dependencies import SessionDep
from src.models import Make, Model, Range, Generation, Configuration
from src.schemas import ScrapeResponse
from src.services.scrape import scrape_makes, scrape_models, scrape_ranges_and_generations, scrape_configurations,\
    UnexpectedDromResponseError


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
        makes = scrape_makes('https://www.drom.ru/catalog')
        time.sleep(1.5)

        makes += scrape_makes('https://www.drom.ru/catalog/lcv')
        time.sleep(1.5)

        for make in makes:
            stmt = select(exists().where(Make.name == make.name))
            if not session.execute(stmt).scalar():
                make_db = Make(name=make.name)
                session.add(make_db)
                session.commit()

            models = scrape_models(make.models_drom_url)
            time.sleep(1.5)

            stmt = select(Make.id).where(Make.name == make.name)
            make_id = session.execute(stmt).scalar()

            for model in models:
                stmt = select(exists().where(and_(Model.make_id == make_id, Model.name == model.name)))
                if not session.execute(stmt).scalar():
                    model_db = Model(name=model.name, type=model.type, make_id=make_id)
                    session.add(model_db)
                    session.commit()

                ranges = scrape_ranges_and_generations(model.ranges_and_generations_drom_url)
                time.sleep(1.5)

                stmt = select(Model.id).where(and_(Model.make_id == make_id, Model.name == model.name))
                model_id = session.execute(stmt).scalar()

                for _range in ranges:
                    stmt = select(exists().where(and_(Range.model_id == model_id, Range.name == model.name)))
                    if not session.execute(stmt).scalar():
                        range_db = Range(name=_range.name, model_id=model_id)
                        session.add(range_db)
                        session.commit()

                    stmt = select(Range.id).where(and_(Range.model_id == model_id, Range.name == _range.name))
                    range_id = session.execute(stmt).scalar()

                    for generation in _range.generations:
                        stmt = select(exists().where(and_(
                            Generation.range_id == range_id, Generation.photo_url == generation.photo_url)))
                        if not session.execute(stmt).scalar():
                            generation_db = Generation(
                                photo_url=generation.photo_url,
                                full_name=generation.full_name,
                                short_name=generation.short_name,
                                vehicle_body=generation.vehicle_body,
                                range_id=range_id
                            )
                            session.add(generation_db)
                            session.commit()

                        url = model.ranges_and_generations_drom_url + generation.configurations_drom_url
                        configurations = scrape_configurations(url)
                        time.sleep(1.5)

                        stmt = select(Generation.id).where(and_(
                                Generation.range_id == range_id, Generation.photo_url == generation.photo_url
                        ))
                        generation_id = session.execute(stmt).scalar()

                        for configuration in configurations:
                            stmt = select(exists().where(and_(
                                Configuration.generation_id == generation_id,
                                Configuration.engine_capacity == configuration.engine_capacity,
                                Configuration.engine_power == configuration.engine_power,
                                Configuration.engine_type == configuration.engine_type,
                                Configuration.transmission == configuration.transmission,
                                Configuration.drive == configuration.drive
                            )))
                            if not session.execute(stmt).scalar():
                                configuration_db = Configuration(
                                    engine_capacity=configuration.engine_capacity,
                                    engine_power=configuration.engine_power,
                                    engine_type=configuration.engine_type,
                                    transmission=configuration.transmission,
                                    drive=configuration.drive,
                                    generation_id=generation_id,
                                )
                                session.add(configuration_db)
                                session.commit()

    except UnexpectedDromResponseError as e:
        return JSONResponse(content={'detail': e.detail, 'drom_response_status_code': e.drom_response_status_code})

    return JSONResponse(content={'detail': 'Data from drom.ru successfully scraped.'})
