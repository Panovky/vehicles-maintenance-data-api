from src.exceptions import ServiceNotFoundException, ServiceInnIsNotUniqueException, ServiceOgrnIsNotUniqueException
from .repository import ServicesRepository
from .schemas import ServiceCreate, ServiceRead, ServiceUpdate


class ServicesService:
    def __init__(self, repository: ServicesRepository):
        self.repository: ServicesRepository = repository

    async def create(self, data: ServiceCreate, manager_id: int) -> ServiceRead:
        if await self.repository.exists(inn=data.inn):
            raise ServiceInnIsNotUniqueException()

        if await self.repository.exists(ogrn=data.ogrn):
            raise ServiceOgrnIsNotUniqueException()

        data_dict = data.model_dump()
        data_dict['manager_id'] = manager_id
        service = await self.repository.create(data_dict)
        return ServiceRead.model_validate(service)

    async def get_manager_services(self, manager_id: int) -> list[ServiceRead]:
        services = await self.repository.filter_by(manager_id=manager_id)
        return [ServiceRead.model_validate(service) for service in services]

    async def update(self, _id: int, data: ServiceUpdate) -> ServiceRead | None:
        data_dict = data.model_dump(exclude_none=True)

        if (summary := data_dict.get('summary')) is not None:
            if summary == '':
                data_dict['summary'] = None

        if (website := data_dict.get('website')) is not None:
            if website == '':
                data_dict['website'] = None

        service = await self.repository.update(_id, data_dict)
        if not service:
            raise ServiceNotFoundException()

        return ServiceRead.model_validate(service)

    async def get_by_id(self, _id: int) -> ServiceRead | None:
        service = await self.repository.get_by_id(_id)
        if not service:
            raise ServiceNotFoundException()
        return ServiceRead.model_validate(service)

    async def get_all(self) -> list[ServiceRead]:
        services = await self.repository.get_all()
        return [ServiceRead.model_validate(service) for service in services]
