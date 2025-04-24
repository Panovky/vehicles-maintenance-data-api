import bcrypt
import jwt
from datetime import timedelta, datetime
from jwt.exceptions import InvalidTokenError
from src.config import settings
from src.exceptions import (
    UserPhoneIsNotUniqueException, UserEmailIsNotUniqueException, InvalidUserCredentialsException,
    InvalidAccessTokenException
)
from src.users.repository import UsersRepository, UserRolesRepository
from src.users.schemas import UserRead
from .schemas import UserRegister, UserLogin, TokenRead


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

    async def get_authenticated_user(self, data: UserLogin) -> UserRead | None:
        user = await self.users_repository.get_by_email(data.email)
        if not user or not self.verify_password(data.password, user.password_hash):
            raise InvalidUserCredentialsException()
        return user

    @staticmethod
    def encode_jwt(
            payload: dict,
            token_expire_minutes: int,
            private_key: str = settings.jwt_auth.private_key_path.read_text(),
            algorithm: str = settings.jwt_auth.algorithm
    ):
        payload_to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=token_expire_minutes)
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

    def get_access_token(self, _id: int, email: str) -> str:
        return self.encode_jwt(
            payload={'sub': str(_id), 'email': email, 'type': 'access'},
            token_expire_minutes=settings.jwt_auth.access_token_expire_minutes
        )

    def get_refresh_token(self, _id: int, email: str) -> str:
        return self.encode_jwt(
            payload={'sub': str(_id), 'email': email, 'type': 'refresh'},
            token_expire_minutes=settings.jwt_auth.refresh_token_expire_days * 24 * 60
        )

    async def register(self, data: UserRegister) -> TokenRead:
        if (phone := data.phone) and await self.users_repository.exists(phone=phone):
            raise UserPhoneIsNotUniqueException()

        if await self.users_repository.exists(email=data.email):
            raise UserEmailIsNotUniqueException()

        data_dict = {key: value for key, value in data.model_dump().items() if key != 'password' and key != 'role'}
        password_hash = self.hash_password(data.password)
        data_dict['password_hash'] = password_hash
        user = await self.users_repository.create(data_dict)

        await self.user_roles_repository.assign_role(user.id, data.role)

        return TokenRead(
            access_token=self.get_access_token(user.id, user.email),
            refresh_token=self.get_refresh_token(user.id, user.email)
        )

    async def login(self, data: UserLogin) -> TokenRead:
        user = await self.get_authenticated_user(data)
        if not user:
            raise

        return TokenRead(
            access_token=self.get_access_token(user.id, user.email),
            refresh_token=self.get_refresh_token(user.id, user.email)
        )

    def refresh(self, user: UserRead) -> TokenRead:
        access_token = self.get_access_token(user.id, user.email)
        return TokenRead(access_token=access_token)

    async def get_current_user_by_token(self, token: str, token_type: str) -> UserRead:
        try:
            payload = self.decode_jwt(token=token)
        except InvalidTokenError:
            raise InvalidAccessTokenException()

        if payload.get('type') != token_type:
            raise InvalidAccessTokenException()

        email = payload.get('email')
        user = await self.users_repository.get_by_email(email)

        if not user:
            raise InvalidAccessTokenException()

        return UserRead(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            birthday=user.birthday,
            phone=user.phone,
            email=user.email,
            roles=[role.role for role in user.roles]
        )
