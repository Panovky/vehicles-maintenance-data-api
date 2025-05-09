from fastapi import APIRouter, Query
from typing import Annotated
from src.dependencies import CurrentOwnerDep, ConfigurationsServiceDep
from .schemas import ConfigurationRead

router = APIRouter(
    prefix='/configurations',
    tags=['configurations']
)


@router.get(
    '',
    responses={
        200: {'description': 'Configurations successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Generation not found'}
    },
    summary='Return a list of configurations by generation id'
)
async def get_configurations(
        current_owner: CurrentOwnerDep,
        generation_id: Annotated[int, Query(gt=0, alias='generation-id')],
        configurations_service: ConfigurationsServiceDep
) -> list[ConfigurationRead]:
    configurations = await configurations_service.get_configurations(generation_id)
    return configurations
