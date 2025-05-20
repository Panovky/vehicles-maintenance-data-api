from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class UserLogin(BaseModel):
    """The model representing the data needed to log in the user."""
    email: Annotated[EmailStr, Field(example="nikita.filatov@yandex.ru")]
    password: Annotated[str, Field(pattern=r'^[A-Za-z0-9-_]{8,16}$', example="2a_B4-cJ_q5")]


class AccessTokenRead(BaseModel):
    """The model representing the access token data to be returned to the client."""
    access_token: str
    token_type: str = 'Bearer'


class AccessRefreshTokensRead(BaseModel):
    """The model representing the access and refresh tokens data to be returned to the client."""
    access_token: str
    refresh_token: str | None = None
    tokens_type: str = 'Bearer'
