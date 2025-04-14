import logging
from dataclasses import dataclass

from src.application.common.pagination.dto import Pagination
from src.application.common.query import Query, QueryHandler
from src.application.user import dto
from src.application.user.interfaces import UserReader
from src.application.user.interfaces.persistence import GetUsersFilters

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetUsers(Query[dto.Users]):
    filters: GetUsersFilters
    pagination: Pagination


class GetUsersHandler(QueryHandler[GetUsers, dto.Users]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUsers) -> dto.Users:
        users = await self._user_reader.get_users(query.filters, query.pagination)
        logger.debug("Get users", extra={"users": users, "pagination": query.pagination, "filters": query.filters})
        return users
