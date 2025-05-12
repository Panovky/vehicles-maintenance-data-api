from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from src.dependencies import AuthServiceDep, CurrentUserByRefreshTokenDep
from .schemas import UserRegister, UserLogin, AccessRefreshTokensRead, AccessTokenRead

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
async def register(data: UserRegister, auth_service: AuthServiceDep) -> AccessRefreshTokensRead:
    return await auth_service.register(data)


@router.get('/verify-email', response_class=RedirectResponse, summary='Verify user email')
async def verify_email(token: str, auth_service: AuthServiceDep) -> RedirectResponse:
    return await auth_service.verify_email(token)


@router.post(
    '/login',
    responses={
        200: {'description': 'User successfully logged in'},
        401: {'description': "User's credentials are invalid"},
        403: {'description': 'User email is not verified'}
    },
    summary='Log in'
)
async def login(data: UserLogin, auth_service: AuthServiceDep) -> AccessRefreshTokensRead:
    return await auth_service.login(data)


@router.post(
    '/refresh-access-token',
    responses={
        200: {'description': 'Access token successfully received'},
        401: {'description': 'Refresh token are invalid'}
    },
    summary='Get access token by refresh token'
)
async def refresh(user: CurrentUserByRefreshTokenDep, auth_service: AuthServiceDep) -> AccessTokenRead:
    return auth_service.refresh(user)
