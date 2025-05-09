from src.generations.repository import GenerationsRepository
from src.exceptions import GenerationNotFoundException
from .repository import ConfigurationsRepository
from .schemas import ConfigurationRead


class ConfigurationsService:
    def __init__(
            self,
            generations_repository: GenerationsRepository,
            configurations_repository: ConfigurationsRepository
    ):
        self.generations_repository: GenerationsRepository = generations_repository
        self.configurations_repository: ConfigurationsRepository = configurations_repository

    async def get_configurations(self, generation_id: int) -> list[ConfigurationRead]:
        if not await self.generations_repository.get_by_id(generation_id):
            raise GenerationNotFoundException()

        configurations = await self.configurations_repository.filter_by(generation_id=generation_id)
        return [ConfigurationRead.model_validate(configuration) for configuration in configurations]

