from dataclasses import dataclass

from src.application.common.user import dto
from src.application.queries.common.query import Query, QueryHandler
from src.domain.user.value_objects import UserId

from .interfaces import UserReader


@dataclass(frozen=True)
class GetUserById(Query[dto.User]):
    user_id: UserId


class GetUserByIdHandler(QueryHandler[GetUserById, dto.User]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUserById) -> dto.User:
        user = await self._user_reader.get_user_by_id(query.user_id)
        return user
