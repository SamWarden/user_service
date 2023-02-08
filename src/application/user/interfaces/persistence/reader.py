from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from src.application.user import dto
from src.domain.base.constants import Empty
from src.domain.user.value_objects import UserId, Username


class GetUsersOrder(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
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

    async def get_users_count(self, deleted: bool | Empty = Empty.UNSET) -> int:
        raise NotImplementedError
