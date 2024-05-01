import dataclasses
from typing import Self

from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user.events import FullNameUpdated
from src.domain.user.events.user_created import UserCreated
from src.domain.user.events.user_deleted import UserDeleted
from src.domain.user.events.username_updated import UsernameUpdated
from src.domain.user.exceptions import UserIsDeletedError, UsernameAlreadyExistsError
from src.domain.user.value_objects import FullName, UserId, Username
from src.domain.user.value_objects.deleted_status import DeletionTime


@dataclasses.dataclass
class User(AggregateRoot):
    id: UserId
    username: Username
    full_name: FullName
    existing_usernames: set[Username] = dataclasses.field(default_factory=set)
    deleted_at: DeletionTime = dataclasses.field(default=DeletionTime.create_not_deleted(), kw_only=True)

    @classmethod
    def create(
        cls,
        user_id: UserId,
        username: Username,
        full_name: FullName,
        existing_usernames: set[Username],
    ) -> Self:
        if username in existing_usernames:
            raise UsernameAlreadyExistsError(username.to_raw())

        existing_usernames.add(username)
        user = cls(user_id, username, full_name, existing_usernames)
        user.record_event(
            UserCreated(
                user_id.to_raw(),
                username.to_raw(),
                full_name.first_name,
                full_name.last_name,
                full_name.middle_name,
            ),
        )
        return user

    def set_username(self, username: Username) -> None:
        self._validate_not_deleted()

        if username != self.username:
            if username in self.existing_usernames:
                raise UsernameAlreadyExistsError(username.to_raw())

            self.existing_usernames.remove(self.username)
            self.existing_usernames.add(username)
            self.username = username
        self.record_event(UsernameUpdated(self.id.to_raw(), self.username.to_raw()))

    def set_full_name(self, full_name: FullName) -> None:
        self._validate_not_deleted()

        self.full_name = full_name
        self.record_event(
            FullNameUpdated(
                self.id.to_raw(),
                self.full_name.first_name,
                self.full_name.last_name,
                self.full_name.middle_name,
            ),
        )

    def delete(self) -> None:
        self._validate_not_deleted()

        self.existing_usernames.remove(self.username)
        self.username = Username(None)
        self.deleted_at = DeletionTime.create_deleted()
        self.record_event(UserDeleted(self.id.to_raw()))

    def _validate_not_deleted(self) -> None:
        if self.deleted_at.is_deleted():
            raise UserIsDeletedError(self.id.to_raw())
