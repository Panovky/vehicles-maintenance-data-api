from fastapi import HTTPException
from starlette import status


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


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь с данным id не найден.'
        )


class UserPhoneIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Пользователь с таким номером телефона уже существует.'
        )


class UserEmailIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Пользователь с таким e-mail уже существует.'
        )


class ServiceNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found.'
        )
