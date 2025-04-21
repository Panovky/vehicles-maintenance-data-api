from src.exceptions import MakeNotFoundException
from .repository import MakesRepository
from .schemas import MakeRead


class MakesService:
    def __init__(self, repository: MakesRepository):
        self.repository: MakesRepository = repository

    async def get_by_id(self, _id: int) -> MakeRead:
        make = await self.repository.get_by_id(_id)
        if not make:
            raise MakeNotFoundException()
        return MakeRead.model_validate(make)

    async def get_all(self) -> list[MakeRead]:
        makes = await self.repository.get_all()
        return [MakeRead.model_validate(make) for make in makes]

    async def starts_with(self, atr_name: str, prefix: str, case_sensitive: bool = False) -> list[MakeRead]:
        makes = await self.repository.starts_with(atr_name, prefix, case_sensitive)
        return [MakeRead.model_validate(make) for make in makes]
