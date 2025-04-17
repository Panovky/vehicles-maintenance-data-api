from fastapi import APIRouter, status
from src.dependencies import AuthServiceDep
from src.users.schemas import UserRead
from .schemas import UserRegister, UserLogin, AccessTokenRead

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
async def register(data: UserRegister, auth_service: AuthServiceDep) -> UserRead:
    user = await auth_service.register(data)
    return user


@router.post(
    '/login',
    responses={
        200: {'description': 'User successfully logged in'},
        401: {'description': "User's credentials are invalid"}
    },
    summary='Log in'
)
async def login(data: UserLogin, auth_service: AuthServiceDep) -> AccessTokenRead:
    access_token = await auth_service.login(data)
    return access_token


@router.post('/refresh')
async def refresh():
    pass


@router.get('/me')
async def me():
    pass
