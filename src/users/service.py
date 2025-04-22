from src.exceptions import UserPhoneIsNotUniqueException, UserNotFoundException, RoleAlreadyExistsForUserException
from .repository import UsersRepository, UserRolesRepository
from .schemas import UserRoleCreate, UserRoleRead, UserUpdate, UserRead


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


class UserRolesService:
    def __init__(self, repository: UserRolesRepository):
        self.repository: UserRolesRepository = repository

    async def assign_role(self, user_id: int, data: UserRoleCreate) -> UserRoleRead:
        if await self.repository.exists(user_id=user_id, role=data.role):
            raise RoleAlreadyExistsForUserException()

        user_role = await self.repository.assign_role(user_id, data.role)
        return UserRoleRead.model_validate(user_role)
