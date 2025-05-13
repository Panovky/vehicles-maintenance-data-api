from src.core.email_service import EmailService
from src.users.repository import UsersRepository
from src.services.repository import ServicesRepository
from .repository import ServiceWorkersRepository


class ServiceWorkersService:
    def __init__(
            self,
            users_repository: UsersRepository,
            services_repository: ServicesRepository,
            service_workers_repository: ServiceWorkersRepository,
            email_service: EmailService
    ):
        self.users_repository: UsersRepository = users_repository
        self.services_repository: ServicesRepository = services_repository
        self.service_workers_repository: ServiceWorkersRepository = service_workers_repository
        self.email_service: EmailService = email_service
