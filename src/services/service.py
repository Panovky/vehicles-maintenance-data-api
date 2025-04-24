from src.exceptions import ServiceNotFoundException
from .repository import ServicesRepository
from .schemas import ServiceCreate, ServiceRead


class ServicesService:
    def __init__(self, repository: ServicesRepository):
        self.repository: ServicesRepository = repository

    async def create(self, data: ServiceCreate, manager_id: int) -> ServiceRead:
        data_dict = data.model_dump()
        data_dict['manager_id'] = manager_id
        service = await self.repository.create(data_dict)
        return ServiceRead.model_validate(service)

    async def get_manager_services(self, manager_id: int) -> list[ServiceRead]:
        services = await self.repository.filter_by(manager_id=manager_id)
        return [ServiceRead.model_validate(service) for service in services]

    async def get_by_id(self, _id: int) -> ServiceRead | None:
        service = await self.repository.get_by_id(_id)
        if not service:
            raise ServiceNotFoundException()
        return ServiceRead.model_validate(service)

    async def get_all(self) -> list[ServiceRead]:
        services = await self.repository.get_all()
        return [ServiceRead.model_validate(service) for service in services]
