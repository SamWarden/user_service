from typing import NoReturn

from sqlalchemy import exists, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from user_service.application.common.exceptions import RepoError
from user_service.application.user.exceptions import UserIdAlreadyExistsError
from user_service.domain.user import entities
from user_service.domain.user.exceptions import UsernameAlreadyExistsError
from user_service.domain.user.interfaces.repo import UserRepo
from user_service.domain.user.value_objects import UserId, Username
from user_service.infrastructure.db.exception_mapper import exception_mapper
from user_service.infrastructure.db.models.user import USERS_TABLE
from user_service.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def acquire_user_by_id(self, user_id: UserId) -> entities.User | None:
        user: entities.User | None = await self._session.get(entities.User, user_id.to_raw(), with_for_update=True)
        return user

    @exception_mapper
    async def add_user(self, user: entities.User) -> None:
        self._session.add(user)
        try:
            await self._session.flush((user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def check_username_exists(self, username: Username) -> bool:
        result: bool | None = await self._session.scalar(
            select(exists().where(USERS_TABLE.c.username == username.to_raw()))
        )
        return result or False

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case "uq_users_username":
                raise UsernameAlreadyExistsError(str(user.username)) from err
            case _:
                raise RepoError from err
