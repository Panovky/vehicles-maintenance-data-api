from fastapi import APIRouter, Query
from typing import Annotated
from src.dependencies import CurrentOwnerDep, GenerationsServiceDep
from .schemas import GenerationRead

router = APIRouter(
    prefix='/generations',
    tags=['generations']
)


@router.get(
    '',
    responses={
        200: {'description': 'Generations successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Range not found'}
    },
    summary='Return a list of generations by range id'
)
async def get_generations(
        current_owner: CurrentOwnerDep,
        range_id: Annotated[int, Query(gt=0, alias='range-id')],
        generations_service: GenerationsServiceDep
) -> list[GenerationRead]:
    generations = await generations_service.get_generations(range_id)
    return generations
