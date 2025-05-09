from src.ranges.repository import RangesRepository
from src.exceptions import RangeNotFoundException
from .repository import GenerationsRepository
from .schemas import GenerationRead


class GenerationsService:
    def __init__(self, ranges_repository: RangesRepository, generations_repository: GenerationsRepository):
        self.ranges_repository: RangesRepository = ranges_repository
        self.generations_repository: GenerationsRepository = generations_repository

    async def get_generations(self, range_id: int) -> list[GenerationRead]:
        if not await self.ranges_repository.get_by_id(range_id):
            raise RangeNotFoundException()

        generations = await self.generations_repository.filter_by(range_id=range_id)
        return [GenerationRead.model_validate(generation) for generation in generations]
