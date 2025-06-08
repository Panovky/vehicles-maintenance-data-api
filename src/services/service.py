from src.exceptions import ServiceNotFoundException, ServiceInnIsNotUniqueException, ServiceOgrnIsNotUniqueException
from src.service_workers.repository import ServiceWorkersRepository
from src.service_clients.repository import ServiceClientsRepository
from .repository import ServicesRepository
from .schemas import ServiceCreate, ServiceRead, ServiceUpdate


class ServicesService:
    def __init__(
            self,
            services_repository: ServicesRepository,
            service_workers_repository: ServiceWorkersRepository,
            service_clients_repository: ServiceClientsRepository
    ):
        self.services_repository: ServicesRepository = services_repository
        self.service_workers_repository: ServiceWorkersRepository = service_workers_repository
        self.service_clients_repository: ServiceClientsRepository = service_clients_repository

    async def create(self, data: ServiceCreate, manager_id: int) -> ServiceRead:
        if await self.services_repository.exists(inn=data.inn):
            raise ServiceInnIsNotUniqueException()

        if await self.services_repository.exists(ogrn=data.ogrn):
            raise ServiceOgrnIsNotUniqueException()

        data_dict = data.model_dump()
        data_dict['manager_id'] = manager_id
        service = await self.services_repository.create(data_dict)
        return ServiceRead.model_validate(service)

    async def get_manager_services(self, manager_id: int) -> list[ServiceRead]:
        services = await self.services_repository.filter_by(manager_id=manager_id)
        return [ServiceRead.model_validate(service) for service in services]

    async def update(self, _id: int, data: ServiceUpdate) -> ServiceRead | None:
        data_dict = data.model_dump(exclude_none=True)

        if (summary := data_dict.get('summary')) is not None:
            if summary == '':
                data_dict['summary'] = None

        if (website := data_dict.get('website')) is not None:
            if website == '':
                data_dict['website'] = None

        service = await self.services_repository.update(_id, data_dict)
        if not service:
            raise ServiceNotFoundException()

        return ServiceRead.model_validate(service)

    async def get_by_id(self, _id: int) -> ServiceRead | None:
        service = await self.services_repository.get_by_id(_id)
        if not service:
            raise ServiceNotFoundException()
        return ServiceRead.model_validate(service)

    async def get_all(self, worker_id: int | None, client_id: int | None) -> list[ServiceRead]:
        if worker_id:
            service_workers = await self.service_workers_repository.filter_by(worker_id=worker_id)
            services = [
                await self.services_repository.get_by_id(service_worker.service_id)
                for service_worker in service_workers
            ]
        elif client_id:
            service_clients = await self.service_clients_repository.filter_by(client_id=client_id)
            services = [
                await self.services_repository.get_by_id(service_client.service_id)
                for service_client in service_clients
            ]
        else:
            services = await self.services_repository.get_all()

        return [ServiceRead.model_validate(service) for service in services]
