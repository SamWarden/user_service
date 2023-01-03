from dataclasses import dataclass

from src.application.base.query import Query, QueryHandler
from src.application.user import dto
from src.application.user.interfaces.persistence import UserReader


@dataclass(frozen=True)
class GetUsers(Query[tuple[dto.User, ...]]):
    pass


class GetUsersHandler(QueryHandler[GetUsers, tuple[dto.User, ...]]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUsers) -> tuple[dto.User, ...]:
        users = await self._user_reader.get_users()
        return users
