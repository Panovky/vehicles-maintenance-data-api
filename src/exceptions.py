from fastapi import HTTPException, status


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
            detail='User not found.'
        )


class UserPhoneIsNotUniqueException(HTTPException):
    def __init__(self, role):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with the same phone number already exists among users with role «{role}».'
        )


class UserEmailIsNotUniqueException(HTTPException):
    def __init__(self, role):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with the same email address already exists among users with role «{role}».'
        )


class UserLoginIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with the same login already exists.'
        )


class ServiceNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found.'
        )
