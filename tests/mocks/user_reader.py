from collections.abc import Sequence
from uuid import UUID

from src.application.user import dto
from src.application.user.exceptions import UserIdNotExist, UsernameNotExist
from src.application.user.interfaces import UserReader
from src.application.user.interfaces.persistence import GetUsersFilters, GetUsersOrder
from src.domain.common.constants import Empty


class UserReaderMock(UserReader):
    def __init__(self):
        self.users: dict[UUID, dto.UserDTOs] = {}

    async def get_user_by_id(self, user_id: UUID) -> dto.UserDTOs:
        if user_id not in self.users:
            raise UserIdNotExist(user_id)

        user = self.users[user_id]
        return user

    async def get_user_by_username(self, username: str) -> dto.User:
        for user in self.users.values():
            if isinstance(user, dto.User) and user.username == username:
                return user
        raise UsernameNotExist(username)

    async def get_users(self, filters: GetUsersFilters) -> list[dto.UserDTOs]:
        users = list(self.users.values())
        if filters.deleted is not Empty.UNSET:
            users = [user for user in users if user.deleted == filters.deleted]
        if filters.order == GetUsersOrder.ASC:
            users.sort(key=lambda user: user.id)
        else:
            users.sort(key=lambda user: user.id, reverse=True)

        offset = filters.offset if filters.offset is not Empty.UNSET else 0
        limit = filters.limit if filters.limit is not Empty.UNSET else len(users)
        last_index = offset + limit
        users = users[offset:last_index]
        return users

    async def get_users_count(self, deleted: bool | Empty = Empty.UNSET) -> int:
        if deleted is not Empty.UNSET:
            count = sum(1 for user in self.users.values() if user.deleted is deleted)
        else:
            count = len(self.users)
        return count

    async def add_user(self, user: dto.UserDTOs) -> None:
        self.users[user.id] = user

    async def add_users(self, users: Sequence[dto.UserDTOs]) -> None:
        for user in users:
            await self.add_user(user)
