from src.exceptions import RoleAlreadyExistsForUserException
from .repository import UserRolesRepository
from .schemas import UserRoleCreate, UserRoleRead


class UserRolesService:
    def __init__(self, repository: UserRolesRepository):
        self.repository: UserRolesRepository = repository

    async def assign_role(self, user_id: int, data: UserRoleCreate) -> UserRoleRead:
        if await self.repository.exists(user_id=user_id, role=data.role):
            raise RoleAlreadyExistsForUserException()

        user_role = await self.repository.assign_role(user_id, data.role)
        return UserRoleRead.model_validate(user_role)
