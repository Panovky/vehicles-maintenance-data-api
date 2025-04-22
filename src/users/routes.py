from fastapi import APIRouter
from src.dependencies import CurrentUserByAccessTokenDep, UsersServiceDep
from .schemas import UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get(
    '/me',
    responses={
        200: {'description': 'Current user successfully received'},
        401: {'description': 'Access token are invalid'}
    },
    summary='Get current user by access token'
)
async def me(user: CurrentUserByAccessTokenDep) -> UserRead:
    return user


@router.patch(
    '/me',
    responses={
        200: {'description': 'Current user successfully updated'},
        401: {'description': 'Access token are invalid'},
        409: {'description': 'Current user data is not unique'}
    },
    summary='Update current user'
)
async def me(user: CurrentUserByAccessTokenDep, data: UserUpdate, users_service: UsersServiceDep) -> UserRead:
    user = await users_service.update(user.id, data)
    return user
