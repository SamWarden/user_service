from typing import NoReturn

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.user import dto
from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.application.user.interfaces.persistence import GetUsersFilters, GetUsersOrder, UserReader, UserRepo
from src.domain.base.constants import Empty
from src.domain.user import entities
from src.domain.user.value_objects import UserId, Username
from src.infrastructure.db.exception_mapper import exception_mapper
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserReaderImpl(SQLAlchemyRepo, UserReader):
    @exception_mapper
    async def get_user_by_id(self, user_id: UserId) -> dto.UserDTOs:
        user = await self._session.scalar(select(User).where(
            User.id == user_id.to_uuid(),
        ))
        if user is None:
            raise UserIdNotExist(user_id.value)

        return self._mapper.load(user, dto.UserDTOs)

    @exception_mapper
    async def get_user_by_username(self, username: Username) -> dto.User:
        user = await self._session.scalar(select(User).where(
            User.username == str(username),
        ))
        if user is None:
            raise UsernameNotExist(username.value)

        return self._mapper.load(user, dto.User)

    @exception_mapper
    async def get_users(self, filters: GetUsersFilters) -> tuple[dto.UserDTOs, ...]:
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
        users = result.all()

        return tuple(self._mapper.load(users, list[dto.UserDTOs]))
        # return self._mapper.load(users, tuple[dto.UserDTOs, ...])


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
        user = await self._session.scalar(select(User).where(
            User.id == user_id.to_uuid(),
        ).with_for_update())
        if user is None:
            raise UserIdNotExist(user_id.value)

        return self._mapper.load(user, entities.User)

    @exception_mapper
    async def add_user(self, user: entities.User) -> None:
        db_user = self._mapper.load(user, User)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def update_user(self, user: entities.User) -> None:
        db_user = self._mapper.load(user, User)
        try:
            await self._session.merge(db_user)
        except IntegrityError as err:
            self._parse_error(err, user)

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:
            case "pk_users":
                raise UserIdAlreadyExists(user.id.value) from err
            case "uq_users_username":
                raise UsernameAlreadyExists(user.username.value) from err
            case _:
                raise RepoError from err
