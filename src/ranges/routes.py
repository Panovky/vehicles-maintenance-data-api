from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select
from typing import Annotated
from src.dependencies import AsyncSessionDep
from src.models.model import Model
from .model import Range
from .schemas import RangeRead

router = APIRouter(
    prefix='/ranges',
    tags=['ranges']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of ranges')
async def get_ranges(
        model_id: Annotated[int, Query(gt=0, alias='model-id')], async_session: AsyncSessionDep
) -> list[RangeRead]:
    """Return a list of all vehicles model ranges for the vehicle model with the specified id."""
    model = await async_session.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle model not found.')
    result = await async_session.execute(select(Range).where(Range.model_id == model_id))
    return result.scalars()
