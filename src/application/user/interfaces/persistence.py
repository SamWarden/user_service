from typing import Protocol

from src.application.user import dto
from src.domain.user.entities import User
from src.domain.user.value_objects import UserId, Username


class UserRepo(Protocol):
    async def add_user(self, user: User) -> None:
        raise NotImplementedError

    async def update_user(self, user: User) -> None:
        raise NotImplementedError

    async def get_user_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UserId) -> dto.User:
        raise NotImplementedError

    async def get_user_by_username(self, username: Username) -> dto.User:
        raise NotImplementedError

    async def get_users(self) -> tuple[dto.User, ...]:
        raise NotImplementedError
