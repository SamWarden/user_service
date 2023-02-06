from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from src.application.user import dto
from src.domain.base.constants import Empty
from src.domain.user import entities
from src.domain.user.value_objects import UserId, Username


class UserRepo(Protocol):
    async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
        raise NotImplementedError

    async def add_user(self, user: entities.User) -> None:
        raise NotImplementedError

    async def update_user(self, user: entities.User) -> None:
        raise NotImplementedError


class GetUsersOrder(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class GetUsersFilters:
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    deleted: bool | Empty = Empty.UNSET
    order: GetUsersOrder = GetUsersOrder.ASC


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UserId) -> dto.UserDTOs:
        raise NotImplementedError

    async def get_user_by_username(self, username: Username) -> dto.User:
        raise NotImplementedError

    async def get_users(self, filters: GetUsersFilters) -> tuple[dto.UserDTOs, ...]:
        raise NotImplementedError
