from fastapi import APIRouter, status
from src.dependencies import AuthServiceDep, CurrentUserByAccessTokenDep
from src.users.schemas import UserRead
from .schemas import UserRegister, UserLogin, TokenRead

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    responses={201: {'description': 'User successfully registered'}, 409: {'description': 'User data is not unique'}},
    summary='Register a user'
)
async def register(data: UserRegister, auth_service: AuthServiceDep) -> TokenRead:
    access_token = await auth_service.register(data)
    return access_token


@router.post(
    '/login',
    responses={
        200: {'description': 'User successfully logged in'},
        401: {'description': "User's credentials are invalid"}
    },
    summary='Log in'
)
async def login(data: UserLogin, auth_service: AuthServiceDep) -> TokenRead:
    access_token = await auth_service.login(data)
    return access_token


@router.post('/refresh')
async def refresh():
    pass


@router.get(
    '/me',
    responses={
        200: {'description': 'User successfully received'},
        401: {'description': 'Access token are invalid'}
    },
    summary='Get current user by access token'
)
async def me(user: CurrentUserByAccessTokenDep) -> UserRead:
    return user
