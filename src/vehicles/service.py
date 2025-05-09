import aiofiles
from pathlib import Path
from fastapi import UploadFile
from src.makes.repository import MakesRepository
from src.models.repository import ModelsRepository
from src.ranges.repository import RangesRepository
from src.generations.repository import GenerationsRepository
from src.configurations.repository import ConfigurationsRepository
from src.exceptions import (
    MakeNotFoundException, ModelNotFoundException, RangeNotFoundException, GenerationNotFoundException,
    ConfigurationNotFoundException, VINIsNotUniqueException, RegistrationPlateIsNotUniqueException
)
from src.config import VEHICLES_PHOTOS_DIR
from .repository import VehiclesRepository
from .schemas import VehicleRead


class VehiclesService:
    def __init__(
        self,
        makes_repository: MakesRepository,
        models_repository: ModelsRepository,
        ranges_repository: RangesRepository,
        generations_repository: GenerationsRepository,
        configurations_repository: ConfigurationsRepository,
        vehicles_repository: VehiclesRepository
    ):
        self.makes_repository: MakesRepository = makes_repository
        self.models_repository: ModelsRepository = models_repository
        self.ranges_repository: RangesRepository = ranges_repository
        self.generations_repository: GenerationsRepository = generations_repository
        self.configurations_repository: ConfigurationsRepository = configurations_repository
        self.vehicles_repository: VehiclesRepository = vehicles_repository

    async def create(self, data: dict, photo: UploadFile | None, owner_id: int) -> VehicleRead:
        if not await self.makes_repository.exists(id=data['make_id']):
            raise MakeNotFoundException()

        if not await self.models_repository.exists(id=data['model_id']):
            raise ModelNotFoundException()

        if not await self.ranges_repository.exists(id=data['range_id']):
            raise RangeNotFoundException()

        if not await self.generations_repository.exists(id=data['generation_id']):
            raise GenerationNotFoundException()

        if not await self.configurations_repository.exists(id=data['configuration_id']):
            raise ConfigurationNotFoundException()

        if await self.vehicles_repository.exists(vin=data['vin']):
            raise VINIsNotUniqueException()

        if await self.vehicles_repository.exists(registration_plate=data['registration_plate']):
            raise RegistrationPlateIsNotUniqueException()

        if photo:
            photo_name = f'{data["vin"]}{Path(photo.filename).suffix}'
            photo_path = VEHICLES_PHOTOS_DIR / photo_name
            async with aiofiles.open(photo_path, 'wb') as buffer:
                while chunk := await photo.read(1024):
                    await buffer.write(chunk)
            data['photo_path'] = f'/static/vehicles/photos/{photo_name}'
        else:
            data['photo_path'] = f'/static/vehicles/photos/default.png'

        data['color'] = data['color'].value
        data['user_id'] = owner_id

        vehicle = await self.vehicles_repository.create(data)
        return VehicleRead.model_validate(vehicle)
