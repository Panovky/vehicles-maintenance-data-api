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


class ServiceWorkerNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Сотрудник автосервиса с указанным id не найден.'
        )


class ServiceClientNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Клиент автосервиса с указанным id не найден.'
        )


class ServiceInnIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Автосервис с указанным ИНН уже существует в системе.'
        )


class ServiceOgrnIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Автосервис с указанным ОГРН (ОГРНИП) уже существует в системе.'
        )


class UnhandledEgrulEgripResponseException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=detail
        )


class ServiceInnNotFoundInEgrulEgripException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Записей в ЕГРЮЛ и ЕГРИП с указанным ИНН не найдено.'
        )


class WorkerIsNotRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Невозможно отправить приглашение в команду, так как пользователь не зарегистрирован в системе.'
        )


class ClientIsNotRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Невозможно отправить приглашение стать клиентом автосервиса, '
                   'так как пользователь не зарегистрирован в системе.'
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


class RangeNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Модельный ряд автомобилей с указанным id не найден.'
        )


class GenerationNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Поколение автомобилей с указанным id не найдено.'
        )


class ConfigurationNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Конфигурация автомобиля с указанным id не найдена.'
        )


class VinIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Автомобиль с таким VIN уже существует в системе.'
        )


class RegistrationPlateIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Автомобиль с таким регистрационным знаком уже существует в системе.'
        )


class VehicleNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Автомобиль с данным id не найден.'
        )


class OwnerIsNotRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Невозможно отправить письмо для передачи истории обслуживания автомобиля новому владельцу,'
                   'поскольку он еще не зарегистрирован в системе.'
        )


class MaintenanceRecordNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Запись о техническом обслуживании автомобиля с указанным id не найдена.'
        )
