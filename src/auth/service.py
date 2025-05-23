import aiofiles
import bcrypt
from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import RedirectResponse
from jwt.exceptions import InvalidTokenError
from src.core.jwt_service import JWTService
from src.core.email_service import EmailService
from src.exceptions import (
    UserEmailIsNotUniqueException, EmailVerifyingPendingException, UserPhoneIsNotUniqueException,
    InvalidUserCredentialsException, UserEmailIsNotVerifiedException, InvalidTokenException
)
from src.users.repository import UsersRepository
from src.users.schemas import UserRead
from src.user_roles.model import UserRoleEnum
from src.user_roles.repository import UserRolesRepository
from src.config import USERS_PHOTOS_DIR
from .schemas import UserLogin, AccessRefreshTokensRead, AccessTokenRead


class AuthService:
    def __init__(
            self,
            users_repository: UsersRepository,
            user_roles_repository: UserRolesRepository,
            jwt_service: JWTService,
            email_service: EmailService
    ):
        self.users_repository: UsersRepository = users_repository
        self.user_roles_repository: UserRolesRepository = user_roles_repository
        self.jwt_service: JWTService = jwt_service
        self.email_service: EmailService = email_service

    @staticmethod
    def hash_password(password: str) -> str:
        password_hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password_hash_bytes.decode()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    async def get_user_by_credentials(self, data: UserLogin) -> UserRead | None:
        user = await self.users_repository.get_by_email(data.email)

        if not user or not self.verify_password(data.password, user.password_hash):
            raise InvalidUserCredentialsException()

        if not user.is_email_verified:
            raise UserEmailIsNotVerifiedException()

        return user

    async def register(self, data: dict, photo: UploadFile | None) -> AccessRefreshTokensRead:
        if res := await self.users_repository.filter_by(email=data['email']):
            if res[0].is_email_verified:
                raise UserEmailIsNotUniqueException()
            else:
                raise EmailVerifyingPendingException()

        if (phone := data['phone']) and await self.users_repository.exists(phone=phone):
            raise UserPhoneIsNotUniqueException()

        data_dict = {key: value for key, value in data.items() if key != 'password' and key != 'role'}
        password_hash = self.hash_password(data['password'])
        data_dict['password_hash'] = password_hash
        data_dict['is_email_verified'] = False

        user = await self.users_repository.create(data_dict)
        await self.user_roles_repository.assign_role(user.id, data['role'])
        if photo:
            photo_name = f'{user.id}{Path(photo.filename).suffix}'
            photo_path = USERS_PHOTOS_DIR / photo_name
            async with aiofiles.open(photo_path, 'wb') as buffer:
                while chunk := await photo.read(1024):
                    await buffer.write(chunk)
            await self.users_repository.update(user.id, {'photo_path': f'/static/users/photos/{photo_name}'})

        name = f'{user.first_name}{" " + patronymic if (patronymic := user.patronymic) else ""}'
        token = self.jwt_service.get_verify_email_token(user.email, data['role'].value)
        url = f'http://localhost:8000/auth/verify-email?token={token}'

        text = self.email_service.get_text_to_verify_email(
            name=name,
            url=url
        )

        html = self.email_service.get_html_to_verify_email(
            name=name,
            url=url
        )

        self.email_service.send_email(
            receiver_address=user.email,
            subject='Завершение регистрации в приложении',
            text=text,
            html=html
        )

        return AccessRefreshTokensRead(
            access_token=self.jwt_service.get_access_token(user.id, user.email),
            refresh_token=self.jwt_service.get_refresh_token(user.id, user.email)
        )

    async def verify_email(self, token: str) -> RedirectResponse:
        try:
            payload = self.jwt_service.decode_jwt(token=token)
        except InvalidTokenError:
            return RedirectResponse(url='http://localhost:4173/register/invalid-token')

        token_type = payload.get('type')
        email = payload.get('sub')
        role = payload.get('role')

        if token_type and token_type == 'verify_email' and email and role:
            if user := await self.users_repository.get_by_email(email):
                await self.users_repository.update(user.id, {'is_email_verified': True})
                url = f'http://localhost:4173/{"vehicles" if role == UserRoleEnum.owner.value else "services"}/create'
                return RedirectResponse(url=url)

        return RedirectResponse(url='http://localhost:4173/register/invalid-token')

    async def login(self, data: UserLogin) -> AccessRefreshTokensRead:
        user = await self.get_user_by_credentials(data)

        return AccessRefreshTokensRead(
            access_token=self.jwt_service.get_access_token(user.id, user.email),
            refresh_token=self.jwt_service.get_refresh_token(user.id, user.email)
        )

    def refresh(self, user: UserRead) -> AccessTokenRead:
        return AccessTokenRead(access_token=self.jwt_service.get_access_token(user.id, user.email))

    async def get_current_user_by_token(self, token: str, token_type: str) -> UserRead:
        try:
            payload = self.jwt_service.decode_jwt(token=token)
        except InvalidTokenError:
            raise InvalidTokenException(token_type)

        if payload.get('type') != token_type:
            raise InvalidTokenException(token_type)

        email = payload.get('email')
        user = await self.users_repository.get_by_email(email)

        if not user:
            raise InvalidTokenException(token_type)

        if token_type == 'access' and not user.is_email_verified:
            raise UserEmailIsNotVerifiedException()

        return UserRead(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            photo_path=user.photo_path,
            birthday=user.birthday,
            phone=user.phone,
            email=user.email,
            roles=[role.role for role in user.roles]
        )
