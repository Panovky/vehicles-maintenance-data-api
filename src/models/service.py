from src.makes.repository import MakesRepository
from src.exceptions import MakeNotFoundException
from .model import ModelTypeEnum
from .repository import ModelsRepository
from .schemas import ModelRead


class ModelsService:
    def __init__(self, makes_repository: MakesRepository, models_repository: ModelsRepository):
        self.makes_repository: MakesRepository = makes_repository
        self.models_repository: ModelsRepository = models_repository

    async def get_models(self, make_id: int, model_type: ModelTypeEnum | None, prefix: str | None) -> list[ModelRead]:
        if not await self.makes_repository.get_by_id(make_id):
            raise MakeNotFoundException()

        if model_type and prefix:
            models = await self.models_repository.get_by_make_id_model_type_and_prefix_alphabetically(
                make_id, model_type, prefix
            )
        elif model_type:
            models = await self.models_repository.get_by_make_id_and_model_type_alphabetically(make_id, model_type)
        elif prefix:
            models = await self.models_repository.get_by_make_id_and_prefix_alphabetically(make_id, prefix)
        else:
            models = await self.models_repository.get_by_make_id_alphabetically(make_id)
        return [ModelRead.model_validate(model) for model in models]
