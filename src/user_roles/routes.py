from fastapi import APIRouter, status
from src.dependencies import CurrentUserByAccessTokenDep, UserRolesServiceDep
from .schemas import UserRoleCreate, UserRoleRead

router = APIRouter(
    tags=['user roles']
)


@router.post(
    '/users/me/roles',
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
