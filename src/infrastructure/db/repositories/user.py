from collections.abc import Iterable
from typing import NoReturn
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.common.pagination.dto import Pagination, PaginationResult, SortOrder
from src.application.user import dto
from src.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError, UsernameNotExistError
from src.application.user.interfaces.persistence import GetUsersFilters, UserReader, UserRepo
from src.domain.common.constants import Empty
from src.domain.user import entities
from src.domain.user.exceptions import UsernameAlreadyExistsError
from src.domain.user.value_objects import UserId, Username
from src.infrastructure.db.converters import (
    convert_db_model_to_active_user_dto,
    convert_db_model_to_user_dto,
    convert_db_model_to_user_entity,
    convert_user_entity_to_db_model,
)
from src.infrastructure.db.exception_mapper import exception_mapper
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserReaderImpl(SQLAlchemyRepo, UserReader):
    @exception_mapper
    async def get_user_by_id(self, user_id: UUID) -> dto.UserDTOs:
        user: User | None = await self._session.get(User, user_id)
        if user is None:
            raise UserIdNotExistError(user_id)

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_user_by_username(self, username: str) -> dto.User:
        user: User | None = await self._session.scalar(select(User).where(User.username == username))
        if user is None:
            raise UsernameNotExistError(username)

        return convert_db_model_to_active_user_dto(user)

    @exception_mapper
    async def get_users(self, filters: GetUsersFilters, pagination: Pagination) -> dto.Users:
        query = select(User)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(User.id.desc())
        else:
            query = query.order_by(User.id.asc())

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(User.deleted_at.is_not(None))
            else:
                query = query.where(User.deleted_at.is_(None))

        if pagination.offset is not Empty.UNSET:
            query = query.offset(pagination.offset)
        if pagination.limit is not Empty.UNSET:
            query = query.limit(pagination.limit)

        result: Iterable[User] = await self._session.scalars(query)
        users = [convert_db_model_to_user_dto(user) for user in result]
        users_count = await self._get_users_count(filters)
        return dto.Users(data=users, pagination=PaginationResult.from_pagination(pagination, total=users_count))

    async def _get_users_count(self, filters: GetUsersFilters) -> int:
        query = select(func.count(User.id))

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(User.deleted_at.is_not(None))
            else:
                query = query.where(User.deleted_at.is_(None))

        users_count: int = await self._session.scalar(query)
        return users_count


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
        user: User | None = await self._session.get(User, user_id.to_raw(), with_for_update=True)
        if user is None:
            raise UserIdNotExistError(user_id.to_raw())

        existing_usernames = await self.get_existing_usernames()
        return convert_db_model_to_user_entity(user, existing_usernames)

    @exception_mapper
    async def add_user(self, user: entities.User) -> None:
        db_user = convert_user_entity_to_db_model(user)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def update_user(self, user: entities.User) -> None:
        db_user = convert_user_entity_to_db_model(user)
        try:
            await self._session.merge(db_user)
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def get_existing_usernames(self) -> set[Username]:
        result: Iterable[str] = await self._session.scalars(select(User.username).where(User.username.is_not(None)))
        existing_usernames = {Username(username) for username in result}
        return existing_usernames

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case "uq_users_username":
                raise UsernameAlreadyExistsError(str(user.username)) from err
            case _:
                raise RepoError from err
