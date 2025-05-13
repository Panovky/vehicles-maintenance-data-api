import jwt
from datetime import timedelta, datetime
from src.config import settings


class JWTService:
    @staticmethod
    def encode_jwt(
            payload: dict,
            token_expire_minutes: int,
            private_key: str = settings.jwt.private_key_path.read_text(),
            algorithm: str = settings.jwt.algorithm
    ) -> str:
        payload_to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=token_expire_minutes)
        payload_to_encode.update(iat=now, exp=expire)
        return jwt.encode(payload_to_encode, private_key, algorithm=algorithm)

    @staticmethod
    def decode_jwt(
            token: str,
            public_key: str = settings.jwt.public_key_path.read_text(),
            algorithm: str = settings.jwt.algorithm
    ) -> str:
        return jwt.decode(token, public_key, algorithms=[algorithm])

    def get_access_token(self, _id: int, email: str) -> str:
        return self.encode_jwt(
            payload={'sub': str(_id), 'email': email, 'type': 'access'},
            token_expire_minutes=settings.jwt.access_token_expire_minutes
        )

    def get_refresh_token(self, _id: int, email: str) -> str:
        return self.encode_jwt(
            payload={'sub': str(_id), 'email': email, 'type': 'refresh'},
            token_expire_minutes=settings.jwt.refresh_token_expire_days * 24 * 60
        )

    def get_verify_email_token(self, email: str, role: str) -> str:
        return self.encode_jwt(
            payload={'sub': email, 'role': role, 'type': 'verify_email'},
            token_expire_minutes=settings.jwt.verify_email_token_expire_hours * 60
        )

    def get_invite_worker_token(self, email: str, position: str) -> str:
        return self.encode_jwt(
            payload={'sub': email, 'position': position, 'type': 'invite_worker'},
            token_expire_minutes=settings.jwt.invite_worker_token_expire_hours * 60
        )
