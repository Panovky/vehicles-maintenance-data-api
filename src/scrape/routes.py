import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select, and_, exists
from src.dependencies import AsyncSessionDep
from src.makes.model import Make
from src.models.model import Model
from src.ranges.model import Range
from src.generations.model import Generation
from src.configurations.model import Configuration
from .schemas import ScrapeResponse
from .service import scrape_makes, scrape_models, scrape_ranges_and_generations, scrape_configurations,\
    UnexpectedDromResponseError, get_unhandled_error_info

router = APIRouter(
    prefix='/scrape',
    tags=['scrape']
)


@router.post('/', responses={200: {'model': ScrapeResponse}}, summary='Scrape drom.ru')
async def scrape_drom_ru(async_session: AsyncSessionDep) -> JSONResponse:
    """
    Scrape vehicles makes, models, models ranges, generations and configurations from drom.ru.

    If there were errors when receiving the response from drom.ru,
    the unhandled_errors field will store information about them.
    """
    unhandled_errors = []

    try:
        makes = scrape_makes('https://www.drom.ru/catalog/')
        time.sleep(1.5)
    except UnexpectedDromResponseError as e:
        unhandled_errors.append(get_unhandled_error_info(e))
        makes = []

    try:
        makes += scrape_makes('https://www.drom.ru/catalog/lcv/')
        time.sleep(1.5)
    except UnexpectedDromResponseError as e:
        unhandled_errors.append(get_unhandled_error_info(e))

    for make in makes:
        stmt = select(exists().where(Make.name == make.name))
        result = await async_session.execute(stmt)
        if not result.scalar():
            make_db = Make(name=make.name)
            async_session.add(make_db)
            await async_session.commit()

        try:
            models = scrape_models(make.models_drom_url)
            time.sleep(1.5)
        except UnexpectedDromResponseError as e:
            unhandled_errors.append(get_unhandled_error_info(e))
            models = []

        stmt = select(Make.id).where(Make.name == make.name)
        result = await async_session.execute(stmt)
        make_id = result.scalar()

        for model in models:
            stmt = select(exists().where(and_(Model.make_id == make_id, Model.name == model.name)))
            result = await async_session.execute(stmt)
            if not result.scalar():
                model_db = Model(name=model.name, type=model.type, make_id=make_id)
                async_session.add(model_db)
                await async_session.commit()

            try:
                ranges = scrape_ranges_and_generations(model.ranges_and_generations_drom_url)
                time.sleep(1.5)
            except UnexpectedDromResponseError as e:
                unhandled_errors.append(get_unhandled_error_info(e))
                ranges = []

            stmt = select(Model.id).where(and_(Model.make_id == make_id, Model.name == model.name))
            result = await async_session.execute(stmt)
            model_id = result.scalar()

            for _range in ranges:
                stmt = select(exists().where(and_(Range.model_id == model_id, Range.name == _range.name)))
                result = await async_session.execute(stmt)
                if not result.scalar():
                    range_db = Range(name=_range.name, model_id=model_id)
                    async_session.add(range_db)
                    await async_session.commit()

                stmt = select(Range.id).where(and_(Range.model_id == model_id, Range.name == _range.name))
                result = await async_session.execute(stmt)
                range_id = result.scalar()

                for generation in _range.generations:
                    stmt = select(exists().where(and_(
                        Generation.range_id == range_id, Generation.photo_url == generation.photo_url)))
                    result = await async_session.execute(stmt)
                    if not result.scalar():
                        generation_db = Generation(
                            photo_url=generation.photo_url,
                            full_name=generation.full_name,
                            short_name=generation.short_name,
                            vehicle_body=generation.vehicle_body,
                            range_id=range_id
                        )
                        async_session.add(generation_db)
                        await async_session.commit()

                    try:
                        configurations = scrape_configurations(generation.configurations_drom_url)
                        time.sleep(1.5)
                    except UnexpectedDromResponseError as e:
                        unhandled_errors.append(get_unhandled_error_info(e))
                        configurations = []

                    stmt = select(Generation.id).where(and_(
                            Generation.range_id == range_id, Generation.photo_url == generation.photo_url
                    ))
                    result = await async_session.execute(stmt)
                    generation_id = result.scalar()

                    for configuration in configurations:
                        stmt = select(exists().where(and_(
                            Configuration.generation_id == generation_id,
                            Configuration.engine_capacity == configuration.engine_capacity,
                            Configuration.engine_power == configuration.engine_power,
                            Configuration.engine_type == configuration.engine_type,
                            Configuration.transmission == configuration.transmission,
                            Configuration.drive == configuration.drive
                        )))
                        result = await async_session.execute(stmt)
                        if not result.scalar():
                            configuration_db = Configuration(
                                engine_capacity=configuration.engine_capacity,
                                engine_power=configuration.engine_power,
                                engine_type=configuration.engine_type,
                                transmission=configuration.transmission,
                                drive=configuration.drive,
                                generation_id=generation_id,
                            )
                            async_session.add(configuration_db)
                            await async_session.commit()

    return JSONResponse(content={
        'detail': 'Data from drom.ru successfully scraped.',
        'unhandled_errors': unhandled_errors
    })
