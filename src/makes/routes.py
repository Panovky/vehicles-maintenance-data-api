from fastapi import APIRouter, Query
from src.dependencies import CurrentOwnerDep, MakesServiceDep
from .schemas import MakeRead
from typing import Annotated

router = APIRouter(
    prefix='/makes',
    tags=['makes']
)


@router.get(
    '',
    responses={
        200: {'description': 'Makes successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Get a list of makes in alphabetical order'
)
async def get_makes(
        current_owner: CurrentOwnerDep,
        makes_service: MakesServiceDep,
        prefix: Annotated[str | None, Query(description='Filter by prefix (case insensitive)')] = None
) -> list[MakeRead]:
    makes = await makes_service.get_makes(prefix)
    return makes
