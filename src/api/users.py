from fastapi import APIRouter, status, Path, Query
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Any, Annotated
from src.database import AsyncSessionDep
from src.exceptions import (
    UserNotFoundException, UserPhoneIsNotUniqueException, UserEmailIsNotUniqueException, UserLoginIsNotUniqueException
)
from src.models import User, UserRoleEnum
from src.schemas import UserRead, UserCreate, UserUpdate
from src.services.users import hash_password

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
        stmt = select(exists().where(and_(
            User.role == user_data.role, User.phone == user_data.phone, User.id != user_id
        )))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise UserPhoneIsNotUniqueException(user_data.role)

    if user_data.email:
        stmt = select(exists().where(and_(
            User.role == user_data.role, User.email == user_data.email, User.id != user_id
        )))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise UserEmailIsNotUniqueException(user_data.role)

    if user_data.login:
        stmt = select(exists().where(and_(User.login == user_data.login, User.id != user_id)))
        result = await async_session.execute(stmt)
        if result.scalar():
            raise UserLoginIsNotUniqueException()

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
        user_role: Annotated[UserRoleEnum | None, Query(alias='user-role')] = None,
        limit: int = 10, offset: int = 0
) -> list[UserRead]:
    """
    Return a list of users with the given role of a given length (limit), starting from a given table entry (offset).
    If no role is specified, a list of users with both roles will be returned.
    """
    if user_role:
        result = await async_session.execute(select(User).where(User.role == user_role).offset(offset).limit(limit))
    else:
        result = await async_session.execute(select(User).offset(offset).limit(limit))
    return result.scalars()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    responses={
        201: {'description': 'User successfully created'},
        409: {'description': 'User data is not unique'}
    },
    summary='Create the user'
)
async def create_user(user_data: UserCreate, async_session: AsyncSessionDep) -> Any:
    """Create the user with the given information."""

    stmt = select(exists().where(and_(User.role == user_data.role, User.phone == user_data.phone)))
    result = await async_session.execute(stmt)
    if result.scalar():
        raise UserPhoneIsNotUniqueException(user_data.role)

    stmt = select(exists().where(and_(User.role == user_data.role, User.email == user_data.email)))
    result = await async_session.execute(stmt)
    if result.scalar():
        raise UserEmailIsNotUniqueException(user_data.role)

    stmt = select(exists().where(and_(User.login == user_data.login)))
    result = await async_session.execute(stmt)
    if result.scalar():
        raise UserLoginIsNotUniqueException()

    user_data_dict = {key: value for key, value in user_data.model_dump().items() if key != 'password'}
    password_hash = hash_password(user_data.password)
    user = User(**user_data_dict, password_hash=password_hash)
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user
