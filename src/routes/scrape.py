from fastapi import APIRouter
from sqlalchemy import select
from src.dependencies import SessionDep
from src.models import Make
from src.services.scrape import scrape_makes


router = APIRouter(
    prefix='/scrape',
    tags=['scrape']
)


@router.post('/', summary='Scrape drom.ru')
def scrape_drom_ru(session: SessionDep):

    makes = scrape_makes('https://www.drom.ru/catalog') + scrape_makes('https://www.drom.ru/catalog/lcv')
    for make in makes:
        if make.name not in session.execute(select(Make.name)).scalars():
            make = Make(name=make.name)
            session.add(make)
            session.commit()
            session.refresh(make)
