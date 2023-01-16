import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.application.common.user import dto
from src.domain.user import entities
from src.domain.user.value_objects import UserId, Username
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserReaderImpl(SQLAlchemyRepo):
    async def get_user_by_id(self, user_id: UserId) -> dto.User:
        user = await self._session.scalar(select(User).where(
            User.id == user_id.to_uuid(),
            User.deleted_at.is_(None),
        ))
        if user is None:
            # TODO: add custom error
            raise ValueError

        return self._mapper.load(user, dto.User)

    async def get_user_by_username(self, username: Username) -> dto.User:
        user = await self._session.scalar(select(User).where(
            User.username == str(username),
            User.deleted_at.is_(None),
        ))
        if user is None:
            # TODO: add custom error
            raise ValueError

        return self._mapper.load(user, dto.User)

    async def get_users(self) -> tuple[dto.User, ...]:
        result = await self._session.scalars(select(User).where(User.deleted_at.is_(None)))
        users = result.all()
        return self._mapper.load(users, tuple[dto.User, ...])


class UserRepoImpl(SQLAlchemyRepo):
    async def get_user_by_id(self, user_id: UserId) -> entities.User:
        user = await self._session.scalar(select(User).where(
            User.id == user_id.to_uuid(),
            User.deleted_at.is_(None),
        ))
        if user is None:
            # TODO: add custom error
            raise ValueError

        return self._mapper.load(user, entities.User)

    async def is_username_exist(self, username: Username) -> bool:
        user = await self._session.scalar(select(User).where(
            User.username == str(username),
            User.deleted_at.is_(None),
        ))
        return user is not None

    async def get_user_by_username(self, username: Username) -> entities.User:
        user = await self._session.scalar(select(User).where(
            User.username == str(username),
            User.deleted_at.is_(None),
        ))
        if user is None:
            # TODO: add custom error
            raise ValueError

        return self._mapper.load(user, entities.User)

    async def add_user(self, user: entities.User) -> None:
        db_user = self._mapper.load(user, User)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            raise ValueError from err

    async def update_user(self, user: entities.User) -> None:
        db_user = self._mapper.load(user, User)
        self._session.add(db_user)
        await self._session.flush((db_user,))

    async def delete_user(self, user: entities.User) -> None:
        db_user = self._mapper.load(user, User)
        db_user.deleted_at = datetime.datetime.now()
        self._session.add(db_user)
        await self._session.flush((db_user,))
