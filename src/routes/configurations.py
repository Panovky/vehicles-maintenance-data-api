from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select
from typing import Annotated
from src.dependencies import SessionDep
from src.models import Generation, Configuration
from src.schemas import ConfigurationRead

router = APIRouter(
    prefix='/configurations',
    tags=['configurations']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of configurations')
def get_configurations(
        generation_id: Annotated[int, Query(gt=0, alias='generation-id')], session: SessionDep
) -> list[ConfigurationRead]:
    """Return a list of all vehicle configurations for the vehicle generation with the specified id."""
    generation = session.get(Generation, generation_id)
    if not generation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vehicle generation not found.')
    configurations = session.execute(
        select(Configuration).where(Configuration.generation_id == generation_id)
    ).scalars()
    return configurations
