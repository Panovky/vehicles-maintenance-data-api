from fastapi import APIRouter, status
from src.dependencies import CurrentUserByAccessTokenDep, UserRolesServiceDep, UsersServiceDep
from .schemas import UserRoleCreate, UserRoleRead, UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post(
    '/me/role',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Role successfully assigned'},
        401: {'description': 'Access token are invalid'},
        409: {'description': 'Role already exists'}
    },
    summary='Assign a new role to the current user'
)
async def me(
        user: CurrentUserByAccessTokenDep, data: UserRoleCreate, user_roles_service: UserRolesServiceDep
) -> UserRoleRead:
    user_roles = await user_roles_service.assign_role(user.id, data)
    return user_roles


@router.get(
    '/me',
    responses={
        200: {'description': 'Current user successfully received'},
        401: {'description': 'Access token are invalid'}
    },
    summary='Get a current user by access token'
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
    summary='Update the current user'
)
async def me(user: CurrentUserByAccessTokenDep, data: UserUpdate, users_service: UsersServiceDep) -> UserRead:
    user = await users_service.update(user.id, data)
    return user
