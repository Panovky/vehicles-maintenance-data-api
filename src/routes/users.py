from fastapi import APIRouter, status, Path, Query
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Any, Annotated
from src.dependencies import SessionDep
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
def get_user(user_id: Annotated[int, Path(gt=0)], session: SessionDep) -> UserRead:
    """Return the user with the specified id."""
    user = session.get(User, user_id)
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
def update_user(user_id: Annotated[int, Path(gt=0)], user_data: UserUpdate, session: SessionDep) -> UserRead:
    """Update the user with the specified id with the given information (blank values are ignored)."""
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException()

    if user_data.phone:
        stmt = select(exists().where(and_(
            User.role == user_data.role, User.phone == user_data.phone, User.id != user_id
        )))
        if session.execute(stmt).scalar():
            raise UserPhoneIsNotUniqueException(user_data.role)

    if user_data.email:
        stmt = select(exists().where(and_(
            User.role == user_data.role, User.email == user_data.email, User.id != user_id
        )))
        if session.execute(stmt).scalar():
            raise UserEmailIsNotUniqueException(user_data.role)

    if user_data.login:
        stmt = select(exists().where(and_(User.login == user_data.login, User.id != user_id)))
        if session.execute(stmt).scalar():
            raise UserLoginIsNotUniqueException()

    for key, value in user_data.model_dump(exclude_none=True).items():
        setattr(user, key, value)

    session.commit()
    session.refresh(user)
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
def delete_user(user_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the user with the specified id."""
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException()
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/', responses={200: {'description': 'Users successfully received'}}, summary='Return a list of users')
def get_users(
        session: SessionDep,
        user_role: Annotated[UserRoleEnum | None, Query(alias='user-role')] = None,
        limit: int = 10, offset: int = 0
) -> list[UserRead]:
    """
    Return a list of users with the given role of a given length (limit), starting from a given table entry (offset).
    If no role is specified, a list of users with both roles will be returned.
    """
    if user_role:
        users = session.execute(select(User).where(User.role == user_role).offset(offset).limit(limit)).scalars()
    else:
        users = session.execute(select(User).offset(offset).limit(limit)).scalars()
    return users


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
def create_user(user_data: UserCreate, session: SessionDep) -> Any:
    """Create the user with the given information."""

    stmt = select(exists().where(and_(User.role == user_data.role, User.phone == user_data.phone)))
    if session.execute(stmt).scalar():
        raise UserPhoneIsNotUniqueException(user_data.role)

    stmt = select(exists().where(and_(User.role == user_data.role, User.email == user_data.email)))
    if session.execute(stmt).scalar():
        raise UserEmailIsNotUniqueException(user_data.role)

    stmt = select(exists().where(and_(User.login == user_data.login)))
    if session.execute(stmt).scalar():
        raise UserLoginIsNotUniqueException()

    user_data_dict = {key: value for key, value in user_data.model_dump().items() if key != 'password'}
    password_hash = hash_password(user_data.password)
    user = User(**user_data_dict, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
