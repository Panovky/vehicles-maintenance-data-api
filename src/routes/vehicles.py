from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select, and_
from typing import Annotated
from src.dependencies import SessionDep
from src.models.vehicles import Make, Model, Range, Generation, Configuration
from src.schemas.vehicles import MakeRead, ModelRead, RangeRead, GenerationRead, ConfigurationRead

router = APIRouter(
    tags=['vehicles']
)


@router.get('/makes/', status_code=status.HTTP_200_OK, summary='Return a list of makes')
def get_makes(session: SessionDep, query: str | None = None) -> list[MakeRead]:
    """
    Return a list of all vehicle makes (the list is sorted alphabetically).
    If the query parameter is specified, only those vehicle makes whose names include this string
    will be returned (string case is irrelevant).
    """
    if query:
        makes = session.execute(select(Make).where(Make.name.ilike(f'%{query}%')).order_by(Make.name)).scalars()
    else:
        makes = session.execute(select(Make).order_by(Make.name)).scalars()
    return makes


@router.get('/models/', status_code=status.HTTP_200_OK, summary='Return a list of models')
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


@router.get('/ranges/', status_code=status.HTTP_200_OK, summary='Return a list of ranges')
def get_ranges(model_id: Annotated[int, Query(gt=0, alias='model-id')], session: SessionDep) -> list[RangeRead]:
    """Return a list of all vehicles model ranges for the vehicle model with the specified id."""
    model = session.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle model not found.')
    ranges = session.execute(select(Range).where(Range.model_id == model_id)).scalars()
    return ranges


@router.get('/generations/', status_code=status.HTTP_200_OK, summary='Return a list of generations')
def get_generations(
        range_id: Annotated[int, Query(gt=0, alias='range-id')], session: SessionDep
) -> list[GenerationRead]:
    """Return a list of all vehicle generations for the vehicles model range with the specified id."""
    _range = session.get(Range, range_id)
    if not _range:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicles model range not found.')
    generations = session.execute(select(Generation).where(Generation.range_id == range_id)).scalars()
    return generations


@router.get('/configurations/', status_code=status.HTTP_200_OK, summary='Return a list of configurations')
def get_configurations(
        generation_id: Annotated[int, Query(gt=0, alias='generation-id')], session: SessionDep
) -> list[ConfigurationRead]:
    """Return a list of all vehicle configurations for the vehicle generation with the specified id."""
    generation = session.get(Generation, generation_id)
    if not generation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle generation not found.')
    configurations = session.execute(
        select(Configuration).where(Configuration.generation_id == generation_id)
    ).scalars()
    return configurations
