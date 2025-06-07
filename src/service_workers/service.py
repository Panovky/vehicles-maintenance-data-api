from fastapi.responses import RedirectResponse
from jwt.exceptions import InvalidTokenError
from src.core.jwt_service import JWTService
from src.core.email_service import EmailService
from src.exceptions import ServiceNotFoundException, WorkerIsNotRegisteredException, ServiceWorkerNotFoundException
from src.users.repository import UsersRepository
from src.user_roles.repository import UserRolesRepository
from src.user_roles.repository import UserRoleEnum
from src.services.repository import ServicesRepository
from .repository import ServiceWorkersRepository
from .schemas import ServiceWorkerInvite, ServiceWorkerRead


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

        name = f'{user.first_name}{" " + patronymic if (patronymic := user.patronymic) else ""}'
        token = self.jwt_service.get_attach_worker_token(data.email, data.position)
        url = f'http://localhost:8000/services/{service_id}/workers/attach?token={token}'

        text = self.email_service.get_text_to_invite_worker(
            name=name,
            commercial_name=service.commercial_name,
            position=data.position,
            url=url
        )

        html = self.email_service.get_html_to_invite_worker(
            name=name,
            commercial_name=service.commercial_name,
            position=data.position,
            url=url
        )

        self.email_service.send_email(
            receiver_address=data.email,
            subject='Приглашение в команду автосервиса',
            text=text,
            html=html
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

    async def rate_service_worker(self, service_id: int, worker_id: int, rating: int) -> None:
        if not await self.services_repository.exists(id=service_id):
            raise ServiceNotFoundException()

        if not await self.users_repository.exists(id=worker_id):
            ServiceWorkerNotFoundException()

        service_workers = await self.service_workers_repository.filter_by(service_id=service_id, worker_id=worker_id)
        service_worker = service_workers[0]

        ratings_sum = service_worker.ratings_sum + rating
        ratings_count = service_worker.ratings_count + 1

        await self.service_workers_repository.update(
            service_worker.id,
            {
                'ratings_sum': ratings_sum,
                'ratings_count': ratings_count,
                'rating': ratings_sum / ratings_count
            }
        )

    async def get_service_workers(self, service_id) -> list[ServiceWorkerRead]:
        if not await self.services_repository.exists(id=service_id):
            raise ServiceNotFoundException()

        service_workers = await self.service_workers_repository.filter_by(service_id=service_id)
        return [
            ServiceWorkerRead(
                id=service_worker.worker.id,
                last_name=service_worker.worker.last_name,
                first_name=service_worker.worker.first_name,
                patronymic=service_worker.worker.patronymic,
                photo_path=service_worker.worker.photo_path,
                phone=service_worker.worker.phone,
                email=service_worker.worker.email,
                position=service_worker.position,
                rating=service_worker.rating
            ) for service_worker in service_workers
        ]

