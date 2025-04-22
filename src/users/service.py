from src.exceptions import UserPhoneIsNotUniqueException, UserNotFoundException
from .repository import UsersRepository
from .schemas import UserUpdate, UserRead


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository: UsersRepository = repository

    async def update(self, _id: int, data: UserUpdate) -> UserRead | None:
        if await self.repository.exists(phone=data.phone):
            raise UserPhoneIsNotUniqueException()

        user = await self.repository.update(_id, data.model_dump(exclude_none=True))
        if not user:
            raise UserNotFoundException()

        return UserRead.model_validate(user)
