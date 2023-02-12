import logging
from dataclasses import dataclass

from src.application.common.query import Query, QueryHandler
from src.application.user import dto
from src.application.user.interfaces import UserReader
from src.application.user.interfaces.persistence import GetUsersFilters, GetUsersOrder
from src.domain.common.constants import Empty

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetUsers(Query[dto.Users]):
    deleted: bool | Empty = Empty.UNSET
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    order: GetUsersOrder = GetUsersOrder.ASC


class GetUsersHandler(QueryHandler[GetUsers, dto.Users]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUsers) -> dto.Users:
        users = await self._user_reader.get_users(GetUsersFilters(
            deleted=query.deleted, offset=query.offset, limit=query.limit, order=query.order,
        ))
        users_count = await self._user_reader.get_users_count(query.deleted)
        logger.debug("Get users", extra={
            "users": users, "total": users_count,
            "offset": query.offset, "limit": query.limit, "deleted": query.deleted,
        })
        return dto.Users(
            users=users,
            total=users_count,
            offset=query.offset,
            limit=query.limit,
        )
