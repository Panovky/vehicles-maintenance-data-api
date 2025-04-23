from src.exceptions import UserPhoneIsNotUniqueException, UserNotFoundException, RoleAlreadyExistsForUserException
from .repository import UsersRepository, UserRolesRepository
from .schemas import UserRoleCreate, UserRoleRead, UserUpdate, UserRead


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository: UsersRepository = repository

    async def update(self, _id: int, data: UserUpdate) -> UserRead | None:
        users_with_same_phone = await self.repository.filter_by(phone=data.phone)
        if any(user.id != _id for user in users_with_same_phone):
            raise UserPhoneIsNotUniqueException()

        user = await self.repository.update(_id, data.model_dump(exclude_none=True))
        if not user:
            raise UserNotFoundException()

        user = await self.repository.get_by_email(user.email)

        return UserRead(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            birthday=user.birthday,
            phone=user.phone,
            email=user.email,
            roles=[role.role for role in user.roles]
        )


class UserRolesService:
    def __init__(self, repository: UserRolesRepository):
        self.repository: UserRolesRepository = repository

    async def assign_role(self, user_id: int, data: UserRoleCreate) -> UserRoleRead:
        if await self.repository.exists(user_id=user_id, role=data.role):
            raise RoleAlreadyExistsForUserException()

        user_role = await self.repository.assign_role(user_id, data.role)
        return UserRoleRead.model_validate(user_role)
