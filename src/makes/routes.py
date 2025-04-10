from fastapi import APIRouter, Path, Query
from src.dependencies import MakesServiceDep
from .schemas import MakeRead
from typing import Annotated

router = APIRouter(
    prefix='/makes',
    tags=['makes']
)


@router.get(
    '/{make_id}',
    responses={200: {'description': 'Make successfully received'}, 404: {'description': 'Make not found'}},
    summary='Get a make by id'
)
async def get_make(make_id: Annotated[int, Path(gt=0)], makes_service: MakesServiceDep) -> MakeRead:
    make = await makes_service.get_by_id(make_id)
    return make


@router.get('/', responses={200: {'description': 'Makes successfully received'}}, summary='Get a list of makes')
async def get_makes(
        makes_service: MakesServiceDep,
        starts_with: Annotated[
            str | None,
            Query(alias='starts-with', description='Filter by prefix (case insensitive)')
        ] = None
) -> list[MakeRead]:
    makes = await makes_service.get_all() if not starts_with else await makes_service.starts_with('name', starts_with)
    return makes
