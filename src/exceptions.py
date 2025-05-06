from fastapi import HTTPException
from starlette import status


class UserEmailIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким email уже существует.'
        )


class EmailVerifyingPendingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='На указанную почту уже выслано письмо для завершения регистрации.'
        )


class UserPhoneIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким номером телефона уже существует.'
        )


class ExpiredVerifyEmailTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_410_GONE,
            detail='Ссылка для подтверждения email устарела. Необходима повторная отправка письма.'
        )


class InvalidVerifyEmailTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверный токен для подтверждения email.'
        )


class InvalidUserCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный email или пароль.'
        )


class UserEmailIsNotVerifiedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Для доступа к приложению завершите регистрацию, перейдя по ссылке в письме.'
        )


class InvalidTokenException(HTTPException):
    def __init__(self, token_type: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Неверный токен {"доступа" if token_type == "access" else "обновления"}.'
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


class ModelNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Модель автомобиля с указанным id не найдена.'
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
