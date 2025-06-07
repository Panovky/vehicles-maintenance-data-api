from datetime import datetime
from src.exceptions import UserPhoneIsNotUniqueException, UserNotFoundException
from .repository import UsersRepository
from .schemas import UserUpdate, UserRead


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository: UsersRepository = repository

    async def update(self, _id: int, data: UserUpdate) -> UserRead | None:
        data_dict = data.model_dump(exclude_none=True)

        if (patronymic := data_dict.get('patronymic')) is not None:
            if patronymic == '':
                data_dict['patronymic'] = None

        if (phone := data_dict.get('phone')) is not None:
            if phone == '':
                data_dict['phone'] = None
            else:
                users_with_same_phone = await self.repository.filter_by(phone=phone)
                if any(user.id != _id for user in users_with_same_phone):
                    raise UserPhoneIsNotUniqueException()

        if (birthday := data_dict.get('birthday')) is not None:
            if birthday == '':
                data_dict['birthday'] = None
            else:
                data_dict['birthday'] = datetime.strptime(birthday, "%Y-%m-%d").date()

        user = await self.repository.update(_id, data_dict)
        if not user:
            raise UserNotFoundException()

        user = await self.repository.get_by_email(user.email)

        return UserRead(
            id=user.id,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            photo_path=user.photo_path,
            birthday=user.birthday,
            phone=user.phone,
            email=user.email,
            roles=[role.role for role in user.roles]
        )
