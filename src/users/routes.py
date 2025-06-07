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
        401: {'description': 'Access token are invalid'},
        403: {'description': 'User email is not verified'}
    },
    summary='Get a current user by access token'
)
async def get_current_user(user: CurrentUserByAccessTokenDep) -> UserRead:
    return user


@router.patch(
    '/me',
    responses={
        200: {'description': 'Current user successfully updated'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'User email is not verified'},
        409: {'description': 'Current user data is not unique'}
    },
    summary='Update the current user'
)
async def update_current_user(
        user: CurrentUserByAccessTokenDep, data: UserUpdate, users_service: UsersServiceDep
) -> UserRead:
    user = await users_service.update(user.id, data)
    return user
