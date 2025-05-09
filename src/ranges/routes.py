from fastapi import APIRouter, Query
from typing import Annotated
from src.dependencies import CurrentOwnerDep, RangesServiceDep
from .schemas import RangeRead

router = APIRouter(
    prefix='/ranges',
    tags=['ranges']
)


@router.get(
    '',
    responses={
        200: {'description': 'Ranges successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Model not found'}
    },
    summary='Get a list of ranges by model id'
)
async def get_ranges(
        current_owner: CurrentOwnerDep,
        model_id: Annotated[int, Query(gt=0, alias='model-id')],
        ranges_service: RangesServiceDep
) -> list[RangeRead]:
    ranges = await ranges_service.get_ranges(model_id)
    return ranges
