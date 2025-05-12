import bcrypt
import jwt
import os
import smtplib
import imaplib
from fastapi.responses import RedirectResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from imapclient import imap_utf7
from datetime import timedelta, datetime
from jwt.exceptions import InvalidTokenError
from src.config import settings
from src.exceptions import (
    UserEmailIsNotUniqueException, EmailVerifyingPendingException, UserPhoneIsNotUniqueException,
    InvalidUserCredentialsException, UserEmailIsNotVerifiedException, InvalidTokenException
)
from src.users.repository import UsersRepository, UserRolesRepository
from src.users.schemas import UserRead, RoleEnum
from .schemas import UserRegister, UserLogin, AccessRefreshTokensRead, AccessTokenRead


class AuthService:
    def __init__(self, users_repository: UsersRepository, user_roles_repository: UserRolesRepository):
        self.users_repository: UsersRepository = users_repository
        self.user_roles_repository: UserRolesRepository = user_roles_repository

    @staticmethod
    def send_email(receiver_address, subject, text, html):
        sender_address = os.getenv('EMAIL_ADDRESS')
        sender_app_password = os.getenv('EMAIL_APP_PASSWORD')
        sender_smtp_server = os.getenv('EMAIL_SMTP_SERVER')
        sender_imap_server = os.getenv('EMAIL_IMAP_SERVER')
        sender_smtp_port = int(os.getenv('EMAIL_SMTP_PORT'))
        sender_imap_port = int(os.getenv('EMAIL_IMAP_PORT'))

        message = MIMEMultipart('alternative')
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = Header(subject, 'utf-8')

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)

        smtp = smtplib.SMTP_SSL(sender_smtp_server, sender_smtp_port)
        smtp.login(sender_address, sender_app_password)
        smtp.sendmail(sender_address, receiver_address, message.as_string())
        smtp.quit()

        imap = imaplib.IMAP4_SSL(sender_imap_server, sender_imap_port)
        imap.login(sender_address, sender_app_password)
        imap.append(
            mailbox=str(imap_utf7.encode('Отправленные'))[2:-1],
            flags=None,
            date_time=None,
            message=message.as_bytes())
        imap.logout()

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

    def get_verify_email_token(self, email: str, role: str) -> str:
        return self.encode_jwt(
            payload={'sub': email, 'role': role, 'type': 'verify_email'},
            token_expire_minutes=settings.jwt_auth.verify_email_token_expire_hours * 60
        )

    async def register(self, data: UserRegister) -> AccessRefreshTokensRead:
        if res := await self.users_repository.filter_by(email=data.email):
            if res[0].is_email_verified:
                raise UserEmailIsNotUniqueException()
            else:
                raise EmailVerifyingPendingException()

        if (phone := data.phone) and await self.users_repository.exists(phone=phone):
            raise UserPhoneIsNotUniqueException()

        data_dict = {key: value for key, value in data.model_dump().items() if key != 'password' and key != 'role'}
        password_hash = self.hash_password(data.password)
        data_dict['password_hash'] = password_hash
        data_dict['is_email_verified'] = False
        user = await self.users_repository.create(data_dict)
        await self.user_roles_repository.assign_role(user.id, data.role)

        name = f'{user.first_name} {patronymic if (patronymic := user.patronymic) else ""}'
        verify_email_token = self.get_verify_email_token(user.email, data.role.value)
        verify_email_url = f'http://localhost:8000/auth/verify-email?token={verify_email_token}'

        self.send_email(
            receiver_address=user.email,
            subject='Завершение регистрации в приложении для управления данными о техническом обслуживании автомобилей',
            text=f"""
            {name}, Вы получили это письмо, 
            так как зарегистрировались в нашем приложении для управления данными о техническом обслуживании автомобилей.

            Для завершения регистрации перейдите по ссылке:
            {verify_email_url}
            (Ссылка действительна в течение 24 часов)
            
            Если ссылка не кликабельна, скопируйте ее и вставьте в адресную строку браузера.
            
            Если Вы не регистрировались в приложении, проигнорируйте это письмо.
            """,
            html=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body style="font-family: Arial, sans-serif; color: #000000 !important; line-height: 1.6;">
                <p>{name}, Вы получили это письмо,
                так как зарегистрировались в нашем приложении 
                для управления данными о техническом обслуживании автомобилей.</p>
                
                <div style="background-color: #adf28d; padding: 15px; border-radius: 4px;">
                    <p>Для завершения регистрации подтвердите Ваш email:</p>
                    <a href="{verify_email_url}" 
                        style="
                            display: inline-block; 
                            padding: 12px 24px;
                            background-color: #f77320; 
                            color: #FFFFFF !important;
                            text-decoration: none; 
                            border-radius: 4px;
                            font-weight: bold; 
                            margin: 5px 0;">Подтвердить email</a>
                    <p>Кнопка активна в течение 24 часов</p>
                </div>
            
                <p>Если кнопка не работает, скопируйте ссылку и вставьте ее в адресную строку браузера:<br>
                <a href="{verify_email_url}">{verify_email_url}</a></p>
            
                <p><em>Если Вы не регистрировались в системе, проигнорируйте это письмо.</em></p>
            </body>
            </html>
            """
        )

        return AccessRefreshTokensRead(
            access_token=self.get_access_token(user.id, user.email),
            refresh_token=self.get_refresh_token(user.id, user.email)
        )

    async def verify_email(self, token: str) -> RedirectResponse:
        try:
            payload = self.decode_jwt(token=token)
        except InvalidTokenError:
            return RedirectResponse(url='http://localhost:4173/register/invalid-token')

        token_type = payload.get('type')
        email = payload.get('sub')
        role = payload.get('role')

        if token_type and token_type == 'verify_email' and email and role:
            if user := await self.users_repository.get_by_email(email):
                await self.users_repository.update(user.id, {'is_email_verified': True})
                url = f'http://localhost:4173/{"vehicles" if role == RoleEnum.owner.value else "services"}/create'
                return RedirectResponse(url=url)

        return RedirectResponse(url='http://localhost:4173/register/invalid-token')

    async def login(self, data: UserLogin) -> AccessRefreshTokensRead:
        user = await self.get_user_by_credentials(data)

        return AccessRefreshTokensRead(
            access_token=self.get_access_token(user.id, user.email),
            refresh_token=self.get_refresh_token(user.id, user.email)
        )

    def refresh(self, user: UserRead) -> AccessTokenRead:
        return AccessTokenRead(access_token=self.get_access_token(user.id, user.email))

    async def get_current_user_by_token(self, token: str, token_type: str) -> UserRead:
        try:
            payload = self.decode_jwt(token=token)
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
            birthday=user.birthday,
            phone=user.phone,
            email=user.email,
            roles=[role.role for role in user.roles]
        )
