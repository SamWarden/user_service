from dataclasses import dataclass

from src.application.common.user import dto
from src.application.queries.common.query import Query, QueryHandler
from src.domain.user.value_objects import Username

from .interfaces import UserReader


@dataclass(frozen=True)
class GetUserByUsername(Query[dto.User]):
    username: Username


class GetUserByUsernameHandler(QueryHandler[GetUserByUsername, dto.User]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUserByUsername) -> dto.User:
        user = await self._user_reader.get_user_by_username(query.username)
        return user
