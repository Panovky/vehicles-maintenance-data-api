from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select, and_
from typing import Annotated
from src.dependencies import SessionDep
from src.models import Make, Model
from src.schemas.vehicles import ModelRead

router = APIRouter(
    prefix='/models',
    tags=['models']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of models')
def get_models(
        make_id: Annotated[int, Query(gt=0, alias='make-id')], session: SessionDep, query: str | None = None
) -> list[ModelRead]:
    """
    Return a list of all vehicle models for the vehicle make with the specified id (the list is sorted alphabetically).
    If the query parameter is specified, only those vehicle models whose names include this string
    will be returned (string case is irrelevant).
    """
    make = session.get(Make, make_id)
    if not make:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle make not found.')
    if query:
        models = session.execute(
            select(Model).where(and_(Model.make_id == make.id, Model.name.ilike(f'%{query}%'))).order_by(Model.name)
        ).scalars()
    else:
        models = session.execute(select(Model).where(Model.make_id == make.id).order_by(Model.name)).scalars()
    return models
