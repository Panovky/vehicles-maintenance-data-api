import aiofiles
import uuid
from jwt.exceptions import InvalidTokenError
from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import RedirectResponse
from src.makes.repository import MakesRepository
from src.models.repository import ModelsRepository
from src.ranges.repository import RangesRepository
from src.generations.repository import GenerationsRepository
from src.configurations.repository import ConfigurationsRepository
from src.users.repository import UsersRepository
from src.user_roles.repository import UserRolesRepository
from src.user_roles.model import UserRoleEnum
from src.exceptions import (
    MakeNotFoundException, ModelNotFoundException, RangeNotFoundException, GenerationNotFoundException,
    ConfigurationNotFoundException, VinIsNotUniqueException, RegistrationPlateIsNotUniqueException,
    VehicleNotFoundException, OwnerIsNotRegisteredException, VehicleOwnerNotFoundException
)
from src.config import VEHICLES_PHOTOS_DIR
from src.core.jwt_service import JWTService
from src.core.email_service import EmailService
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
        vehicles_repository: VehiclesRepository,
        users_repository: UsersRepository,
        user_roles_repository: UserRolesRepository,
        jwt_service: JWTService,
        email_service: EmailService
    ):
        self.makes_repository: MakesRepository = makes_repository
        self.models_repository: ModelsRepository = models_repository
        self.ranges_repository: RangesRepository = ranges_repository
        self.generations_repository: GenerationsRepository = generations_repository
        self.configurations_repository: ConfigurationsRepository = configurations_repository
        self.vehicles_repository: VehiclesRepository = vehicles_repository
        self.users_repository: UsersRepository = users_repository
        self.user_roles_repository: UserRolesRepository = user_roles_repository
        self.jwt_service: JWTService = jwt_service
        self.email_service: EmailService = email_service

    async def init_vehicle_transfer(self, vehicle_id: int, email: str) -> None:
        if not (vehicle := await self.vehicles_repository.get_by_id(vehicle_id)):
            raise VehicleNotFoundException()

        if not (user := await self.users_repository.get_by_email(email)) or not user.is_email_verified:
            raise OwnerIsNotRegisteredException()

        name = f'{user.first_name}{" " + patronymic if (patronymic := user.patronymic) else ""}'
        make = vehicle.make.name
        model = vehicle.model.name
        registration_plate = vehicle.registration_plate
        token = self.jwt_service.get_transfer_vehicle_token(email)
        url = f'http://localhost:8000/vehicles/{vehicle_id}/transfer?token={token}'

        text = self.email_service.get_text_to_init_vehicle_transfer(
            name=name,
            make=make,
            model=model,
            registration_plate=registration_plate,
            url=url
        )

        html = self.email_service.get_html_to_init_vehicle_transfer(
            name=name,
            make=make,
            model=model,
            registration_plate=registration_plate,
            url=url
        )

        self.email_service.send_email(
            receiver_address=email,
            subject='Передача истории технического обслуживания автомобиля',
            text=text,
            html=html
        )

    async def transfer_vehicle(self, vehicle_id: int, token: str) -> RedirectResponse:
        try:
            payload = self.jwt_service.decode_jwt(token=token)
        except InvalidTokenError:
            return RedirectResponse(url='http://localhost:4173/transfer/invalid-token')

        token_type = payload.get('type')
        email = payload.get('sub')

        if token_type and token_type == 'transfer_vehicle' and email:
            user = await self.users_repository.get_by_email(email)

            if not await self.user_roles_repository.exists(user_id=user.id, role=UserRoleEnum.owner):
                await self.user_roles_repository.assign_role(user.id, UserRoleEnum.owner)

            await self.vehicles_repository.update(vehicle_id, {'owner_id': user.id})

            return RedirectResponse(url=f'http://localhost:4173/vehicles/{vehicle_id}')

        return RedirectResponse(url='http://localhost:4173/attach/invalid-token')

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
            raise VinIsNotUniqueException()

        if await self.vehicles_repository.exists(registration_plate=data['registration_plate']):
            raise RegistrationPlateIsNotUniqueException()

        if photo:
            photo_name = f'{uuid.uuid4().hex}{Path(photo.filename).suffix}'
            photo_path = VEHICLES_PHOTOS_DIR / photo_name
            async with aiofiles.open(photo_path, 'wb') as buffer:
                while chunk := await photo.read(1024):
                    await buffer.write(chunk)
            data['photo_path'] = f'/static/vehicles/photos/{photo_name}'

        data['color'] = data['color'].value
        data['owner_id'] = owner_id

        vehicle = await self.vehicles_repository.create(data)
        return VehicleRead.model_validate(vehicle)

    async def get_owner_vehicles(self, owner_id: int) -> list[VehicleRead]:
        if not await self.users_repository.exists(id=owner_id):
            raise VehicleOwnerNotFoundException()

        vehicles = await self.vehicles_repository.filter_by(owner_id=owner_id)
        return [VehicleRead.model_validate(vehicle) for vehicle in vehicles]
