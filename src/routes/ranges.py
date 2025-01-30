from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select
from typing import Annotated
from src.dependencies import SessionDep
from src.models import Model, Range
from src.schemas import RangeRead

router = APIRouter(
    prefix='/ranges',
    tags=['ranges']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of ranges')
def get_ranges(model_id: Annotated[int, Query(gt=0, alias='model-id')], session: SessionDep) -> list[RangeRead]:
    """Return a list of all vehicles model ranges for the vehicle model with the specified id."""
    model = session.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle model not found.')
    ranges = session.execute(select(Range).where(Range.model_id == model_id)).scalars()
    return ranges
