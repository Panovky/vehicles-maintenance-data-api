from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select, and_
from typing import Annotated
from src.dependencies import AsyncSessionDep
from src.makes.model import Make
from .model import Model, ModelTypeEnum
from .schemas import ModelRead

router = APIRouter(
    prefix='/models',
    tags=['models']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of models')
async def get_models(
        make_id: Annotated[int, Query(gt=0, alias='make-id')],
        async_session: AsyncSessionDep,
        model_type: Annotated[ModelTypeEnum | None, Query(alias='model-type')] = None,
        query: str | None = None
) -> list[ModelRead]:
    """
    Return a list of all vehicle models for the vehicle make with the specified id (the list is sorted alphabetically).

    If model_type parameter is specified, only vehicle models with this type will be returned.
    If no model_type is specified, a list of vehicle models with both types will be returned.

    If the query parameter is specified, only those vehicle models whose names include this string
    will be returned (string case is irrelevant).
    """
    make = await async_session.get(Make, make_id)
    if not make:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle make not found.')
    if model_type:
        if query:
            result = await async_session.execute(
                select(Model)
                .where(and_(Model.make_id == make.id, Model.type == model_type, Model.name.ilike(f'%{query}%')))
                .order_by(Model.name)
            )
        else:
            result = await async_session.execute(
                select(Model)
                .where(and_(Model.make_id == make.id, Model.type == model_type))
                .order_by(Model.name)
            )
    else:
        if query:
            result = await async_session.execute(
                select(Model)
                .where(and_(Model.make_id == make.id, Model.name.ilike(f'%{query}%')))
                .order_by(Model.name)
            )
        else:
            result = await async_session.execute(
                select(Model)
                .where(Model.make_id == make.id)
                .order_by(Model.name)
            )
    return result.scalars()
