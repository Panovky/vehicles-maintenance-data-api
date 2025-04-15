import bcrypt
import jwt
from src.config import settings
from src.users.repository import UsersRepository


class AuthService:
    def __init__(self, repository: UsersRepository):
        self.repository: UsersRepository = repository

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

    async def register(self):
        pass
