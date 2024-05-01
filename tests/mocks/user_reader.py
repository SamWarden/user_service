from collections.abc import Sequence
from uuid import UUID

from src.application.common.pagination.dto import Pagination, PaginationResult, SortOrder
from src.application.user import dto
from src.application.user.exceptions import UserIdNotExistError, UsernameNotExistError
from src.application.user.interfaces import UserReader
from src.application.user.interfaces.persistence import GetUsersFilters
from src.domain.common.constants import Empty


class UserReaderMock(UserReader):
    def __init__(self) -> None:
        self.users: dict[UUID, dto.UserDTOs] = {}

    async def get_user_by_id(self, user_id: UUID) -> dto.UserDTOs:
        if user_id not in self.users:
            raise UserIdNotExistError(user_id)

        user = self.users[user_id]
        return user

    async def get_user_by_username(self, username: str) -> dto.User:
        for user in self.users.values():
            if isinstance(user, dto.User) and user.username == username:
                return user
        raise UsernameNotExistError(username)

    async def get_users(self, filters: GetUsersFilters, pagination: Pagination) -> dto.Users:
        users = list(self.users.values())
        if filters.deleted is not Empty.UNSET:
            if filters.deleted is True:
                users = [user for user in users if user.deleted_at is not None]
            else:
                users = [user for user in users if user.deleted_at is None]
        if pagination.order == SortOrder.ASC:
            users.sort(key=lambda user: user.id)
        else:
            users.sort(key=lambda user: user.id, reverse=True)

        offset = pagination.offset if pagination.offset is not Empty.UNSET else 0
        limit = pagination.limit if pagination.limit is not Empty.UNSET else len(users)
        last_index = offset + limit
        users = users[offset:last_index]
        users_count = await self._get_users_count(filters)
        return dto.Users(data=users, pagination=PaginationResult.from_pagination(pagination, total=users_count))

    async def _get_users_count(self, filters: GetUsersFilters) -> int:
        if filters.deleted is not Empty.UNSET:
            if filters.deleted is True:
                count = sum(1 for user in self.users.values() if user.deleted_at is not None)
            else:
                count = sum(1 for user in self.users.values() if user.deleted_at is None)
        else:
            count = len(self.users)
        return count

    async def add_user(self, user: dto.UserDTOs) -> None:
        self.users[user.id] = user

    async def add_users(self, users: Sequence[dto.UserDTOs]) -> None:
        for user in users:
            await self.add_user(user)
