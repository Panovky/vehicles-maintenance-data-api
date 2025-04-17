from fastapi import APIRouter, status
from src.dependencies import AuthServiceDep
from src.users.schemas import UserRead
from .schemas import UserRegister, UserLogin

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


@router.post('/login')
async def login(data: UserLogin, auth_service: AuthServiceDep):
    res = auth_service.login()
    return res


@router.post('/refresh')
async def refresh():
    pass


@router.get('/me')
async def me():
    pass
