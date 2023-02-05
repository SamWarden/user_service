from dataclasses import dataclass
from uuid import UUID

from src.application.common.query import Query, QueryHandler
from src.application.user import dto
from src.application.user.interfaces import UserReader
from src.domain.user.value_objects import UserId


@dataclass(frozen=True)
class GetUserById(Query[dto.UserDTOs]):
    user_id: UUID


class GetUserByIdHandler(QueryHandler[GetUserById, dto.UserDTOs]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUserById) -> dto.UserDTOs:
        user = await self._user_reader.get_user_by_id(UserId(query.user_id))
        return user
