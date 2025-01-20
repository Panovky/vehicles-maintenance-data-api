from fastapi import APIRouter, HTTPException, status, Path
from fastapi.responses import Response
from sqlalchemy import select
from typing import Any, Annotated
from src.dependencies import SessionDep
from src.models.user import User
from src.schemas.users import UserRead, UserCreate, UserUpdate
from src.services.users import hash_password

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def check_user_data_uniqueness(user_data: UserCreate | UserUpdate, session: SessionDep) -> None:
    if user_data.phone and user_data.phone in session.execute(select(User.phone)).scalars().all():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with the same phone number already exists.'
        )
    if user_data.email and user_data.email in session.execute(select(User.email)).scalars().all():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with the same email address already exists.'
        )
    if user_data.login and user_data.login in session.execute(select(User.login)).scalars().all():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with the same login already exists.'
        )


@router.get('/{user_id}', status_code=status.HTTP_200_OK, summary='Return the user')
def get_user(user_id: Annotated[int, Path(gt=0)], session: SessionDep) -> UserRead:
    """Return the user with the specified id."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    return user


@router.patch('/{user_id}', status_code=status.HTTP_200_OK, summary='Update the user')
def update_user(user_id: Annotated[int, Path(gt=0)], user_data: UserUpdate, session: SessionDep) -> UserRead:
    """Update the user with the specified id with the given information (blank values are ignored)."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    check_user_data_uniqueness(user_data, session)
    for key, value in user_data.model_dump(exclude_none=True).items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete the user')
def delete_user(user_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the user with the specified id."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/', status_code=status.HTTP_200_OK, summary='Return a list of users')
def get_users(session: SessionDep, limit: int = 10, offset: int = 0) -> list[UserRead]:
    """Return a list of users of a given length (limit), starting from a given table entry (offset)."""
    users = session.execute(select(User).offset(offset).limit(limit)).scalars().all()
    return users


@router.post('/', response_model=UserRead, status_code=status.HTTP_201_CREATED, summary='Create the user')
def create_user(user_data: UserCreate, session: SessionDep) -> Any:
    """Create the user with the given information."""
    check_user_data_uniqueness(user_data, session)
    user_data_dict = {key: value for key, value in user_data.model_dump().items() if key != 'password'}
    password_hash = hash_password(user_data.password)
    user = User(**user_data_dict, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
