from user_service.application.user.exceptions import UserIdNotExistError
from user_service.domain.common.service import BaseService
from user_service.domain.user import entities
from user_service.domain.user.events import FullNameUpdated, UserCreated, UserDeleted, UsernameUpdated
from user_service.domain.user.exceptions import UserIsDeletedError, UsernameAlreadyExistsError
from user_service.domain.user.interfaces.repo import UserRepo
from user_service.domain.user.value_objects import FullName, UserId, Username
from user_service.domain.user.value_objects.deletion_time import DeletionTime


class UserService(BaseService):
    def __init__(self, user_repo: UserRepo) -> None:
        super().__init__()
        self._user_repo = user_repo

    async def create_user(
        self,
        user_id: UserId,
        username: Username,
        full_name: FullName,
    ) -> entities.User:
        username_exists = await self._user_repo.check_username_exists(username)
        if username_exists:
            raise UsernameAlreadyExistsError(username.to_raw())

        user = entities.User(user_id, username, full_name)
        await self._user_repo.add_user(user)
        self._record_event(
            UserCreated(
                user_id.to_raw(),
                username.to_raw(),
                full_name.first_name,
                full_name.last_name,
                full_name.middle_name,
            ),
        )
        return user

    async def set_user_username(self, user_id: UserId, username: Username) -> None:
        user = await self._user_repo.acquire_user_by_id(user_id)
        if user is None:
            raise UserIdNotExistError(user_id.to_raw())
        self._validate_user_not_deleted(user)

        if username != user.username:
            await self._ensure_username_not_exist(username)
            user.username = username

        self._record_event(UsernameUpdated(user.id.to_raw(), user.username.to_raw()))

    async def set_user_full_name(self, user_id: UserId, full_name: FullName) -> None:
        user = await self._user_repo.acquire_user_by_id(user_id)
        if user is None:
            raise UserIdNotExistError(user_id.to_raw())
        self._validate_user_not_deleted(user)

        user.full_name = full_name

        self._record_event(
            FullNameUpdated(
                user.id.to_raw(),
                user.full_name.first_name,
                user.full_name.last_name,
                user.full_name.middle_name,
            ),
        )

    async def delete_user(self, user_id: UserId) -> None:
        user = await self._user_repo.acquire_user_by_id(user_id)
        if user is None:
            raise UserIdNotExistError(user_id.to_raw())
        self._validate_user_not_deleted(user)

        user.username = Username(None)
        user.deleted_at = DeletionTime.create_deleted()

        self._record_event(UserDeleted(user.id.to_raw()))

    async def _ensure_username_not_exist(self, username: Username) -> None:
        username_exists = await self._user_repo.check_username_exists(username)
        if username_exists:
            raise UsernameAlreadyExistsError(username.to_raw())

    def _validate_user_not_deleted(self, user: entities.User) -> None:
        if user.deleted_at.is_deleted():
            raise UserIsDeletedError(user.id.to_raw())
