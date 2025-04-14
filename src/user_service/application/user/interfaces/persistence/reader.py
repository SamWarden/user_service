from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from user_service.application.common.pagination.dto import Pagination
from user_service.application.user import dto
from user_service.domain.common.constants import Empty


@dataclass(frozen=True)
class GetUsersFilters:
    deleted: bool | Empty = Empty.UNSET


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UUID) -> dto.User | None:
        raise NotImplementedError

    async def get_user_by_username(self, username: str) -> dto.User | None:
        raise NotImplementedError

    async def get_users(self, filters: GetUsersFilters, pagination: Pagination) -> dto.Users:
        raise NotImplementedError
