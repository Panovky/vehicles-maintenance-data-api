from fastapi import APIRouter, Query
from typing import Annotated
from src.dependencies import CurrentOwnerDep, ModelsServiceDep
from .model import ModelTypeEnum
from .schemas import ModelRead

router = APIRouter(
    prefix='/models',
    tags=['models']
)


@router.get(
    '',
    responses={
        200: {'description': 'Models successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'},
        404: {'description': 'Make not found'}
    },
    summary='Get a list of models by make id in alphabetical order'
)
async def get_models(
        current_owner: CurrentOwnerDep,
        make_id: Annotated[int, Query(gt=0, alias='make-id')],
        models_service: ModelsServiceDep,
        model_type: Annotated[
            ModelTypeEnum | None,
            Query(alias='model-type', description='Filter by model type')
        ] = None,
        prefix: Annotated[str | None, Query(description='Filter by prefix (case insensitive)')] = None
) -> list[ModelRead]:
    models = await models_service.get_models(make_id, model_type, prefix)
    return models
