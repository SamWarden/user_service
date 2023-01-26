from typing import Protocol

from src.application.user import dto
from src.domain.user import entities
from src.domain.user.value_objects import UserId, Username


class UserRepo(Protocol):
    async def get_user_by_id(self, user_id: UserId) -> entities.User:
        raise NotImplementedError

    async def add_user(self, user: entities.User) -> None:
        raise NotImplementedError

    async def update_user(self, user: entities.User) -> None:
        raise NotImplementedError


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UserId) -> dto.UserDTOs:
        raise NotImplementedError

    async def get_user_by_username(self, username: Username) -> dto.UserDTOs:
        raise NotImplementedError

    async def get_users(self) -> tuple[dto.UserDTOs, ...]:
        raise NotImplementedError
