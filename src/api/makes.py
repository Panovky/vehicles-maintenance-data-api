from fastapi import APIRouter, status
from sqlalchemy import select
from src.dependencies import AsyncSessionDep
from src.models import Make
from src.schemas import MakeRead

router = APIRouter(
    prefix='/makes',
    tags=['makes']
)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of makes')
async def get_makes(async_session: AsyncSessionDep, query: str | None = None) -> list[MakeRead]:
    """
    Return a list of all vehicle makes (the list is sorted alphabetically).
    If the query parameter is specified, only those vehicle makes whose names include this string
    will be returned (string case is irrelevant).
    """
    if query:
        result = await async_session.execute(select(Make).where(Make.name.ilike(f'%{query}%')).order_by(Make.name))
    else:
        result = await async_session.execute(select(Make).order_by(Make.name))
    return result.scalars()
