from fastapi import HTTPException
from starlette import status


class InvalidUserCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный e-mail или пароль.'
        )


class InvalidAccessTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный токен доступа.'
        )


class UserPhoneIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким номером телефона уже существует.'
        )


class UserEmailIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким e-mail уже существует.'
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь с данным id не найден.'
        )


class RoleAlreadyExistsForUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже обладает данной ролью.',
        )


class AccessDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав для выполнения данного действия.',
        )


class ServiceNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Автосервис с указанным id не найден.'
        )


class MakeNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Марка автомобиля с указанным id не найдена.'
        )


class VehicleNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vehicle not found.'
        )


class VINIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Vehicle with the same VIN already exists.'
        )


class RegistrationNumberIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Vehicle with the same registration number already exists.'
        )
