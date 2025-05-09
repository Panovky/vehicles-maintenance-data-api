from src.models.repository import ModelsRepository
from src.exceptions import ModelNotFoundException
from .repository import RangesRepository
from .schemas import RangeRead


class RangesService:
    def __init__(self, models_repository: ModelsRepository, ranges_repository: RangesRepository):
        self.models_repository: ModelsRepository = models_repository
        self.ranges_repository: RangesRepository = ranges_repository

    async def get_ranges(self, model_id: int) -> list[RangeRead]:
        if not await self.models_repository.get_by_id(model_id):
            raise ModelNotFoundException()

        ranges = await self.ranges_repository.filter_by(model_id=model_id)
        return [RangeRead.model_validate(_range) for _range in ranges]
