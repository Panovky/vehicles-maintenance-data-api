import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta, datetime
from src.config import settings
from src.users.model import User
from src.users.repository import UsersRepository, UserRolesRepository
from src.users.schemas import UserRead
from src.exceptions import (
    UserPhoneIsNotUniqueException, UserEmailIsNotUniqueException, InvalidUserCredentialsException,
    InvalidAccessTokenException
)
from .schemas import UserRegister, UserLogin, AccessTokenRead


class AuthService:
    def __init__(self, users_repository: UsersRepository, user_roles_repository: UserRolesRepository):
        self.users_repository: UsersRepository = users_repository
        self.user_roles_repository: UserRolesRepository = user_roles_repository

    @staticmethod
    def hash_password(password: str) -> str:
        password_hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password_hash_bytes.decode()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    async def get_authenticated_user(self, data: UserLogin) -> User | None:
        user = await self.users_repository.get_by_email(data.email)
        if not user or not self.verify_password(data.password, user.password_hash):
            raise InvalidUserCredentialsException()
        return user

    @staticmethod
    def encode_jwt(
            payload: dict,
            private_key: str = settings.jwt_auth.private_key_path.read_text(),
            algorithm: str = settings.jwt_auth.algorithm,
            access_token_expire_minutes: int = settings.jwt_auth.access_token_expire_minutes,
            access_token_expire_timedelta: timedelta | None = None
    ):
        payload_to_encode = payload.copy()
        now = datetime.utcnow()
        if access_token_expire_timedelta:
            expire = now + access_token_expire_timedelta
        else:
            expire = now + timedelta(minutes=access_token_expire_minutes)
        payload_to_encode.update(iat=now, exp=expire)
        encoded = jwt.encode(payload_to_encode, private_key, algorithm=algorithm)
        return encoded

    @staticmethod
    def decode_jwt(
            token: str,
            public_key: str = settings.jwt_auth.public_key_path.read_text(),
            algorithm: str = settings.jwt_auth.algorithm
    ):
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded

    async def register(self, data: UserRegister) -> UserRead:
        if await self.users_repository.exists(phone=data.phone):
            raise UserPhoneIsNotUniqueException()

        if await self.users_repository.exists(email=data.email):
            raise UserEmailIsNotUniqueException()

        data_dict = {key: value for key, value in data.model_dump().items() if key != 'password' and key != 'role_id'}
        password_hash = self.hash_password(data.password)
        data_dict['password_hash'] = password_hash
        user = await self.users_repository.create(data_dict)

        await self.user_roles_repository.assign_role(user.id, data.role_id)

        return UserRead.model_validate(user)

    async def login(self, data: UserLogin) -> AccessTokenRead:
        user = await self.get_authenticated_user(data)
        if not user:
            raise

        payload = {'sub': str(user.id), 'email': user.email}
        access_token = self.encode_jwt(payload=payload)
        return AccessTokenRead(access_token=access_token, token_type='Bearer')

    async def get_current_user_by_access_token(self, access_token: str) -> UserRead:
        try:
            payload = self.decode_jwt(token=access_token)
        except InvalidTokenError:
            raise InvalidAccessTokenException()

        email = payload.get('email')
        user = await self.users_repository.get_by_email(email)

        if not user:
            raise InvalidAccessTokenException()
        return UserRead.model_validate(user)
