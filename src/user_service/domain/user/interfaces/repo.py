import abc
from typing import Protocol

from user_service.domain.user import entities
from user_service.domain.user.value_objects import UserId, Username


class UserRepo(Protocol):
    @abc.abstractmethod
    async def acquire_user_by_id(self, user_id: UserId) -> entities.User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_user(self, user: entities.User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def check_username_exists(self, username: Username) -> bool:
        raise NotImplementedError
