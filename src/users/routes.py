from fastapi import APIRouter, status
from src.dependencies import (
    CurrentUserByAccessTokenDep, UserRolesServiceDep, UsersServiceDep, CurrentManagerDep, ServicesServiceDep
)
from src.services.schemas import ServiceRead
from .schemas import UserRoleCreate, UserRoleRead, UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post(
    '/me/roles',
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Role successfully assigned'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'User email is not verified'},
        409: {'description': 'Role already exists'}
    },
    summary='Assign a new role to the current user'
)
async def assign_role(
        user: CurrentUserByAccessTokenDep, data: UserRoleCreate, user_roles_service: UserRolesServiceDep
) -> UserRoleRead:
    user_roles = await user_roles_service.assign_role(user.id, data)
    return user_roles


@router.get(
    '/me/services',
    tags=['services'],
    responses={
        200: {'description': 'Services successfully received'},
        401: {'description': 'Access token are invalid'},
        403: {'description': 'Access for current user denied'}
    },
    summary='Get current manager services'
)
async def get_manager_services(
        current_manager: CurrentManagerDep, services_service: ServicesServiceDep
) -> list[ServiceRead]:
    services = await services_service.get_manager_services(current_manager.id)
    return services


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
