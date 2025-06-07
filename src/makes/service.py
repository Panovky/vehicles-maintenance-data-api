from .repository import MakesRepository
from .schemas import MakeRead


class MakesService:
    def __init__(self, repository: MakesRepository):
        self.repository: MakesRepository = repository

    async def get_makes(self, prefix: str | None) -> list[MakeRead]:
        if prefix:
            makes = await self.repository.get_by_prefix_alphabetically(prefix)
        else:
            makes = await self.repository.get_all_alphabetically()
        return [MakeRead.model_validate(make) for make in makes]
