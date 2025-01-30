from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select
from typing import Annotated
from src.dependencies import SessionDep
from src.models import Range, Generation
from src.schemas import GenerationRead

router = APIRouter(
    prefix='/generations',
    tags=['generations']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of generations')
def get_generations(
        range_id: Annotated[int, Query(gt=0, alias='range-id')], session: SessionDep
) -> list[GenerationRead]:
    """Return a list of all vehicle generations for the vehicles model range with the specified id."""
    _range = session.get(Range, range_id)
    if not _range:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicles model range not found.')
    generations = session.execute(select(Generation).where(Generation.range_id == range_id)).scalars()
    return generations
