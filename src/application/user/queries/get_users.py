from dataclasses import dataclass

from src.application.common.query import Query, QueryHandler
from src.application.user import dto
from src.application.user.interfaces import UserReader
from src.application.user.interfaces.persistence import GetUsersFilters, GetUsersOrder
from src.domain.base.constants import Empty


@dataclass(frozen=True)
class GetUsers(Query[tuple[dto.UserDTOs, ...]]):
    deleted: bool | Empty = Empty.UNSET
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    order: GetUsersOrder = GetUsersOrder.ASC


class GetUsersHandler(QueryHandler[GetUsers, tuple[dto.UserDTOs, ...]]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUsers) -> tuple[dto.UserDTOs, ...]:
        users = await self._user_reader.get_users(GetUsersFilters(
            deleted=query.deleted, offset=query.offset, limit=query.limit, order=query.order,
        ))
        return users
