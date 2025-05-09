from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / 'static'
VEHICLES_PHOTOS_DIR = STATIC_DIR / 'vehicles' / 'photos'


class JWTAuth(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'
    verify_email_token_expire_hours: int = 24
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    jwt_auth: JWTAuth = JWTAuth()


settings = Settings()
