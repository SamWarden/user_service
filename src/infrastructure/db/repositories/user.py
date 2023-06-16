from typing import NoReturn
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.user import dto
from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.application.user.interfaces.persistence import GetUsersFilters, GetUsersOrder, UserReader, UserRepo
from src.domain.common.constants import Empty
from src.domain.user import entities
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
            raise UserIdNotExist(user_id)

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_user_by_username(self, username: str) -> dto.User:
        user: User | None = await self._session.scalar(
            select(User).where(
                User.username == username,
            )
        )
        if user is None:
            raise UsernameNotExist(username)

        return convert_db_model_to_active_user_dto(user)

    @exception_mapper
    async def get_users(self, filters: GetUsersFilters) -> list[dto.UserDTOs]:
        query = select(User)

        if filters.order is GetUsersOrder.DESC:
            query = query.order_by(User.id.desc())
        else:
            query = query.order_by(User.id.asc())

        if filters.deleted is not Empty.UNSET:
            query = query.where(User.deleted == filters.deleted)

        if filters.offset is not Empty.UNSET:
            query = query.offset(filters.offset)
        if filters.limit is not Empty.UNSET:
            query = query.limit(filters.limit)

        result = await self._session.scalars(query)
        users: list[User] = list(result)

        return [convert_db_model_to_user_dto(user) for user in users]

    async def get_users_count(self, deleted: bool | Empty = Empty.UNSET) -> int:
        query = select(func.count(User.id))

        if deleted is not Empty.UNSET:
            query = query.where(User.deleted == deleted)

        users_count: int = await self._session.scalar(query)
        return users_count or 0


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
        user: User | None = await self._session.get(User, user_id.to_uuid(), with_for_update=True)
        if user is None:
            raise UserIdNotExist(user_id.to_uuid())

        return convert_db_model_to_user_entity(user)

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
    async def check_user_exists(self, user_id: UserId) -> bool:
        user_exists: bool = await self._session.scalar(
            select(select(User).where(User.id == user_id.to_uuid()).exists())
        )
        return user_exists

    @exception_mapper
    async def check_username_exists(self, username: Username) -> bool:
        username_exists: bool = await self._session.scalar(
            select(select(User).where(User.username == str(username)).exists())
        )
        return username_exists

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExists(user.id.to_uuid()) from err
            case "uq_users_username":
                raise UsernameAlreadyExists(str(user.username)) from err
            case _:
                raise RepoError from err
