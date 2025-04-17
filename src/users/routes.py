from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select, exists
from typing import Annotated
from src.dependencies import AsyncSessionDep
from src.utils.exceptions import (
    UserNotFoundException, UserPhoneIsNotUniqueException, UserEmailIsNotUniqueException
)
from .model import User
from .schemas import UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get(
    '/{user_id}',
    responses={200: {'description': 'User successfully received'}, 404: {'description': 'User not found'}},
    summary='Return the user'
)
async def get_user(user_id: Annotated[int, Path(gt=0)], async_session: AsyncSessionDep) -> UserRead:
    """Return the user with the specified id."""
    user = await async_session.get(User, user_id)
    if not user:
        raise UserNotFoundException()
    return user


@router.patch(
    '/{user_id}',
    responses={
        200: {'description': 'User successfully updated'},
        404: {'description': 'User not found'},
        409: {'description': 'User data is not unique'}
    },
    summary='Update the user'
)
async def update_user(
        user_id: Annotated[int, Path(gt=0)], user_data: UserUpdate, async_session: AsyncSessionDep
) -> UserRead:
    """Update the user with the specified id with the given information (blank values are ignored)."""
    user = await async_session.get(User, user_id)
    if not user:
        raise UserNotFoundException()

    if user_data.phone:
        stmt = select(exists().where(User.phone == user_data.phone))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise UserPhoneIsNotUniqueException(user_data.role)

    if user_data.email:
        stmt = select(exists().where(User.email == user_data.email))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise UserEmailIsNotUniqueException(user_data.role)

    for key, value in user_data.model_dump(exclude_none=True).items():
        setattr(user, key, value)

    await async_session.commit()
    await async_session.refresh(user)
    return user


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'User successfully deleted'},
        404: {'description': 'User not found'},
    },
    summary='Delete the user'
)
async def delete_user(user_id: Annotated[int, Path(gt=0)], async_session: AsyncSessionDep) -> Response:
    """Delete the user with the specified id."""
    user = await async_session.get(User, user_id)
    if not user:
        raise UserNotFoundException()
    await async_session.delete(user)
    await async_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/', responses={200: {'description': 'Users successfully received'}}, summary='Return a list of users')
async def get_users(
        async_session: AsyncSessionDep,
        limit: int = 10, offset: int = 0
) -> list[UserRead]:
    result = await async_session.execute(select(User).offset(offset).limit(limit))
    return result.scalars()
