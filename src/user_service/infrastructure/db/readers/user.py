from collections.abc import Iterable
from typing import Any
from uuid import UUID

from sqlalchemy import func, select

from user_service.application.common.pagination.dto import Pagination, PaginationResult, SortOrder
from user_service.application.user import dto
from user_service.application.user.interfaces.persistence import GetUsersFilters, UserReader
from user_service.domain.common.constants import Empty
from user_service.infrastructure.db.converters.user import convert_db_row_to_user_dto
from user_service.infrastructure.db.exception_mapper import exception_mapper
from user_service.infrastructure.db.models.user import USERS_TABLE
from user_service.infrastructure.db.readers.base import SQLAlchemyReader


class UserReaderImpl(SQLAlchemyReader, UserReader):
    @exception_mapper
    async def get_user_by_id(self, user_id: UUID) -> dto.User | None:
        result = await self._session.execute(select(USERS_TABLE).where(USERS_TABLE.c.id == user_id))
        user_row = result.mappings().one_or_none()
        if user_row is None:
            return None

        return convert_db_row_to_user_dto(user_row)

    @exception_mapper
    async def get_user_by_username(self, username: str) -> dto.User | None:
        result = await self._session.execute(select(USERS_TABLE).where(USERS_TABLE.c.username == username))
        user_row = result.mappings().one_or_none()
        if user_row is None:
            return None

        return convert_db_row_to_user_dto(user_row)

    @exception_mapper
    async def get_users(self, filters: GetUsersFilters, pagination: Pagination) -> dto.Users:
        query = select(USERS_TABLE)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(USERS_TABLE.c.id.desc())
        else:
            query = query.order_by(USERS_TABLE.c.id.asc())

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(USERS_TABLE.c.deleted_at.is_not(None))
            else:
                query = query.where(USERS_TABLE.c.deleted_at.is_(None))

        if pagination.offset is not Empty.UNSET:
            query = query.offset(pagination.offset)
        if pagination.limit is not Empty.UNSET:
            query = query.limit(pagination.limit)

        users_rows: Iterable[Any] = await self._session.execute(query)
        users = [convert_db_row_to_user_dto(user_row) for user_row in users_rows]
        users_count = await self._get_users_count(filters)
        return dto.Users(data=users, pagination=PaginationResult.from_pagination(pagination, total=users_count))

    async def _get_users_count(self, filters: GetUsersFilters) -> int:
        query = select(func.count(USERS_TABLE.c.id))

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(USERS_TABLE.c.deleted_at.is_not(None))
            else:
                query = query.where(USERS_TABLE.c.deleted_at.is_(None))

        users_count: int = await self._session.scalar(query)
        return users_count
