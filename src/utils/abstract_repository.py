from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, _id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, _id: int, data: dict) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, _id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def filter_by(self, **filters) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, **filters) -> bool:
        raise NotImplementedError
