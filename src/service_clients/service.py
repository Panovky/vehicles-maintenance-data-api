from fastapi.responses import RedirectResponse
from jwt.exceptions import InvalidTokenError
from src.core.jwt_service import JWTService
from src.core.email_service import EmailService
from src.exceptions import ServiceNotFoundException, ClientIsNotRegisteredException
from src.users.repository import UsersRepository
from src.user_roles.repository import UserRolesRepository
from src.user_roles.repository import UserRoleEnum
from src.services.repository import ServicesRepository
from .repository import ServiceClientsRepository
from .schemas import ServiceClientRead


class ServiceClientsService:
    def __init__(
            self,
            users_repository: UsersRepository,
            user_roles_repository: UserRolesRepository,
            services_repository: ServicesRepository,
            service_clients_repository: ServiceClientsRepository,
            jwt_service: JWTService,
            email_service: EmailService
    ):
        self.users_repository: UsersRepository = users_repository
        self.user_roles_repository: UserRolesRepository = user_roles_repository
        self.services_repository: ServicesRepository = services_repository
        self.service_clients_repository: ServiceClientsRepository = service_clients_repository
        self.jwt_service: JWTService = jwt_service
        self.email_service: EmailService = email_service

    async def invite_client(self, service_id: int, email: str) -> None:
        if not (service := await self.services_repository.get_by_id(service_id)):
            raise ServiceNotFoundException()

        if not (user := await self.users_repository.get_by_email(email)) or not user.is_email_verified:
            raise ClientIsNotRegisteredException()

        name = f'{user.first_name}{" " + patronymic if (patronymic := user.patronymic) else ""}'
        token = self.jwt_service.get_attach_client_token(email)
        url = f'http://localhost:8000/services/{service_id}/clients/attach?token={token}'

        text = self.email_service.get_text_to_invite_client(
            name=name,
            commercial_name=service.commercial_name,
            url=url
        )

        html = self.email_service.get_html_to_invite_client(
            name=name,
            commercial_name=service.commercial_name,
            url=url
        )

        self.email_service.send_email(
            receiver_address=email,
            subject='Приглашение стать клиентом автосервиса',
            text=text,
            html=html
        )

    async def attach_client(self, service_id: int, token: str) -> RedirectResponse:
        try:
            payload = self.jwt_service.decode_jwt(token=token)
        except InvalidTokenError:
            return RedirectResponse(url='http://localhost:4173/attach/invalid-token')

        token_type = payload.get('type')
        email = payload.get('sub')

        if token_type and token_type == 'attach_client' and email:
            user = await self.users_repository.get_by_email(email)

            if not await self.user_roles_repository.exists(user_id=user.id, role=UserRoleEnum.owner):
                await self.user_roles_repository.assign_role(user.id, UserRoleEnum.owner)

            await self.service_clients_repository.create({
                'service_id': service_id,
                'client_id': user.id,
            })
            return RedirectResponse(url=f'http://localhost:4173/services/{service_id}')

        return RedirectResponse(url='http://localhost:4173/attach/invalid-token')

    async def get_service_clients(self, service_id: int) -> list[ServiceClientRead]:
        if not await self.services_repository.exists(id=service_id):
            raise ServiceNotFoundException()

        service_clients = await self.service_clients_repository.filter_by(service_id=service_id)
        return [
            ServiceClientRead(
                id=service_client.client.id,
                last_name=service_client.client.last_name,
                first_name=service_client.client.first_name,
                patronymic=service_client.client.patronymic,
                photo_path=service_client.client.photo_path,
                phone=service_client.client.phone,
                email=service_client.client.email
            ) for service_client in service_clients
        ]
