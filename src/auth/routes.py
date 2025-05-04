from fastapi import APIRouter, status, Response
from src.dependencies import AuthServiceDep, CurrentUserByRefreshTokenDep
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


@router.get(
    '/verify-email',
    responses={
        204: {'description': 'User email successfully verified'},
        400: {'description': 'Verify email token is invalid'},
        410: {'description': 'Verify email token expired'},
    },
    summary='Verify user email'
)
async def verify_email(token: str, auth_service: AuthServiceDep) -> Response:
    await auth_service.verify_email(token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/login',
    responses={
        200: {'description': 'User successfully logged in'},
        401: {'description': "User's credentials are invalid"},
        403: {'description': 'User email is not verified'}
    },
    summary='Log in'
)
async def login(data: UserLogin, auth_service: AuthServiceDep) -> TokenRead:
    access_token = await auth_service.login(data)
    return access_token


@router.post(
    '/refresh',
    responses={
        200: {'description': 'Access token successfully received'},
        401: {'description': 'Refresh token are invalid'}
    },
    response_model=TokenRead,
    response_model_exclude_none=True,
    summary='Get access token by refresh token'
)
async def refresh(user: CurrentUserByRefreshTokenDep, auth_service: AuthServiceDep):
    return auth_service.refresh(user)
