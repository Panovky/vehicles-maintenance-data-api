from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select
from typing import Annotated
from src.dependencies import AsyncSessionDep
from src.ranges.model import Range
from .model import Generation
from .schemas import GenerationRead

router = APIRouter(
    prefix='/generations',
    tags=['generations']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of generations')
async def get_generations(
        range_id: Annotated[int, Query(gt=0, alias='range-id')], async_session: AsyncSessionDep
) -> list[GenerationRead]:
    """Return a list of all vehicle generations for the vehicles model range with the specified id."""
    _range = await async_session.get(Range, range_id)
    if not _range:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicles model range not found.')
    result = await async_session.execute(select(Generation).where(Generation.range_id == range_id))
    return result.scalars()
