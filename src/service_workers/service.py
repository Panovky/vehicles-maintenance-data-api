from fastapi.responses import RedirectResponse
from jwt.exceptions import InvalidTokenError
from src.core.jwt_service import JWTService
from src.core.email_service import EmailService
from src.exceptions import ServiceNotFoundException, WorkerIsNotRegisteredException
from src.users.repository import UsersRepository
from src.user_roles.repository import UserRolesRepository
from src.user_roles.repository import UserRoleEnum
from src.services.repository import ServicesRepository
from .repository import ServiceWorkersRepository
from .schemas import ServiceWorkerInvite


class ServiceWorkersService:
    def __init__(
            self,
            users_repository: UsersRepository,
            user_roles_repository: UserRolesRepository,
            services_repository: ServicesRepository,
            service_workers_repository: ServiceWorkersRepository,
            jwt_service: JWTService,
            email_service: EmailService
    ):
        self.users_repository: UsersRepository = users_repository
        self.user_roles_repository: UserRolesRepository = user_roles_repository
        self.services_repository: ServicesRepository = services_repository
        self.service_workers_repository: ServiceWorkersRepository = service_workers_repository
        self.jwt_service: JWTService = jwt_service
        self.email_service: EmailService = email_service

    async def invite_worker(self, service_id: int, data: ServiceWorkerInvite) -> None:
        if not (service := await self.services_repository.get_by_id(service_id)):
            raise ServiceNotFoundException()

        if not (user := await self.users_repository.get_by_email(data.email)) or not user.is_email_verified:
            raise WorkerIsNotRegisteredException()

        name = f'{user.first_name} {patronymic if (patronymic := user.patronymic) else ""}'
        attach_worker_token = self.jwt_service.get_attach_worker_token(data.email, data.position)
        attach_worker_url = \
            f'http://localhost:8000/services/{service_id}/workers/attach?token={attach_worker_token}'

        self.email_service.send_email(
            receiver_address=data.email,
            subject='Приглашение в команду автосервиса',
            text=f"""
            Здравствуйте, {name}!  
            
            Вас приглашают в команду автосервиса «{service.commercial_name}» на должность «{data.position}».  

            Для подтверждения перейдите по ссылке: 
            {attach_worker_url} 
            (Ссылка действительна в течение 24 часов) 
            
            Если ссылка не кликабельна, скопируйте ее и вставьте в адресную строку браузера.
            
            Если письмо пришло Вам по ошибке, проигнорируйте его.  
            """,
            html=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body style="font-family: Arial, sans-serif; color: #000000 !important; line-height: 1.6;">
                <p>Здравствуйте, {name}!  
                
                <br>Вас приглашают в команду автосервиса «{service.commercial_name}» на должность «{data.position}».</p>

                <div style="background-color: #adf28d; padding: 15px; border-radius: 4px;">
                    <a href="{attach_worker_url}" 
                        style="
                            display: inline-block; 
                            padding: 12px 24px;
                            background-color: #f77320; 
                            color: #FFFFFF !important;
                            text-decoration: none; 
                            border-radius: 4px;
                            font-weight: bold; 
                            margin: 5px 0;">Принять приглашение</a>
                    <p>Кнопка активна в течение 24 часов</p>
                </div>

                <p>Если кнопка не работает, скопируйте ссылку и вставьте ее в адресную строку браузера:<br>
                <a href="{attach_worker_url}">{attach_worker_url}</a></p>

                <p><em>Если письмо пришло Вам по ошибке, проигнорируйте его.</em></p>
            </body>
            </html>
            """
        )

    async def attach_worker(self, service_id: int, token: str) -> RedirectResponse:
        try:
            payload = self.jwt_service.decode_jwt(token=token)
        except InvalidTokenError:
            return RedirectResponse(url='http://localhost:4173/attach/invalid-token')

        token_type = payload.get('type')
        email = payload.get('sub')
        position = payload.get('position')

        if token_type and token_type == 'attach_worker' and email and position:
            user = await self.users_repository.get_by_email(email)

            if not await self.user_roles_repository.exists(user_id=user.id, role=UserRoleEnum.worker):
                await self.user_roles_repository.assign_role(user.id, UserRoleEnum.worker)

            await self.service_workers_repository.create({
                'service_id': service_id,
                'worker_id': user.id,
                'position': position
            })
            return RedirectResponse(url=f'http://localhost:4173/services/{service_id}')

        return RedirectResponse(url='http://localhost:4173/attach/invalid-token')
