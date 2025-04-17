from fastapi import APIRouter, status
from src.dependencies import AuthServiceDep
from src.users.schemas import UserCreate, UserRead

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
async def register(data: UserCreate, auth_service: AuthServiceDep) -> UserRead:
    user = await auth_service.register(data)
    return user


@router.post('/login')
async def login():
    pass


@router.post('/refresh')
async def refresh():
    pass


@router.get('/me')
async def me():
    pass
