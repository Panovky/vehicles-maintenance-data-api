import bcrypt
import jwt
from src.config import settings
from src.users.repository import UsersRepository, UserRolesRepository
from src.users.schemas import UserCreate, UserRead
from src.exceptions import UserPhoneIsNotUniqueException, UserEmailIsNotUniqueException


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

    @staticmethod
    def encode_jwt(
            payload: dict,
            private_key: str = settings.jwt_auth.private_key_path.read_text(),
            algorithm: str = settings.jwt_auth.algorithm
    ):
        encoded = jwt.encode(payload, private_key, algorithm=algorithm)
        return encoded

    @staticmethod
    def decode_jwt(
            jwt_token: str,
            public_key: str = settings.jwt_auth.public_key_path.read_text(),
            algorithm: str = settings.jwt_auth.algorithm
    ):
        decoded = jwt.decode(jwt_token, public_key, algorithms=[algorithm])
        return decoded

    async def register(self, data: UserCreate) -> UserRead:
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
