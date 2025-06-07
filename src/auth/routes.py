from datetime import date
from fastapi import APIRouter, status, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Annotated
from pydantic import EmailStr
from src.dependencies import AuthServiceDep, CurrentUserByRefreshTokenDep
from .schemas import UserLogin, AccessRefreshTokensRead, AccessTokenRead
from src.user_roles.model import UserRoleEnum

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
async def register(
        last_name: Annotated[str, Form(max_length=100)],
        first_name: Annotated[str, Form(max_length=50)],
        email: Annotated[EmailStr, Form()],
        password: Annotated[str, Form(pattern=r'^[A-Za-z0-9-_]{8,16}$')],
        role: Annotated[UserRoleEnum, Form()],
        auth_service: AuthServiceDep,
        phone: Annotated[str | None, Form(pattern=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$')] = None,
        birthday: Annotated[date | None, Form()] = None,
        patronymic: Annotated[str | None, Form(max_length=40)] = None,
        photo: Annotated[UploadFile | None, File()] = None
) -> AccessRefreshTokensRead:
    return await auth_service.register(
        {
            'last_name': last_name,
            'first_name': first_name,
            'patronymic': patronymic,
            'birthday': birthday,
            'phone': phone,
            'email': email,
            'password': password,
            'role': role
        },
        photo
    )


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
