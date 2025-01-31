import time
from fastapi import APIRouter
from sqlalchemy import select
from src.dependencies import SessionDep
from src.models import Make, Model
from src.services.scrape import scrape_makes, scrape_models


router = APIRouter(
    prefix='/scrape',
    tags=['scrape']
)


@router.post('/', summary='Scrape drom.ru')
def scrape_drom_ru(session: SessionDep):

    scrapped_makes = scrape_makes('https://www.drom.ru/catalog') + scrape_makes('https://www.drom.ru/catalog/lcv')
    for scrapped_make in scrapped_makes:
        if scrapped_make.name not in session.execute(select(Make.name)).scalars():
            make = Make(name=scrapped_make.name)
            session.add(make)
            session.commit()

        make_id = session.execute(select(Make.id).where(Make.name == scrapped_make.name)).scalar()
        scrapped_models = scrape_models(scrapped_make.models_drom_url)
        for scrapped_model in scrapped_models:
            if scrapped_model.name not in session.execute(select(Model.name).where(Model.make_id == make_id)).scalars():
                model = Model(name=scrapped_model.name, type=scrapped_model.type, make_id=make_id)
                session.add(model)
                session.commit()
        time.sleep(1.5)
